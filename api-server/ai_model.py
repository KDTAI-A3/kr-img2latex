from transformers import AutoTokenizer, BertForSequenceClassification, BertConfig, BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cosine
from torchvision import transforms
from keras.utils import pad_sequences
from transformers import (
    DonutProcessor,
    VisionEncoderDecoderConfig,
    VisionEncoderDecoderModel
)

from PIL import Image
import torch
import glob
import numpy as np
import re
import easyocr
import json
import matplotlib.pyplot as plt


LABEL_TO_KR = {
    "e":'초',
    "m":'중',
    "h":'고'
}

class CFG:
    seed_val = 42

    max_length = 350 # temp length
    image_height = 480
    image_width = 480


np.random.seed(CFG.seed_val)
torch.manual_seed(CFG.seed_val)
torch.cuda.manual_seed_all(CFG.seed_val)


## Main 모델입니다.
class LatexGenerator:
    '''
    Description:
        LatexGenerator class for img2latex generation. Uses Donut fine-tuned model.
    Parameter:
        pretrained_path: pretrained_path of the donut model. The path must contain model, processor, config files.
    Return:
        None
     '''
    def __init__(self, pretrained_path: str):
        self.pretrained_path = pretrained_path
        self.reader = easyocr.Reader(['en', 'ko'], gpu=True)
        self.config = None
        self.processor = None
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.initialize()

    def initialize(self):
        '''
        Description:
            Initializing Donut fine-tuned model from pretrained_path.
        Parameter:
            None
        Return:
            None
        '''
        self.processor = DonutProcessor.from_pretrained(self.pretrained_path+'processor')
        self.config = VisionEncoderDecoderConfig.from_pretrained(self.pretrained_path+'config')
        self.model = VisionEncoderDecoderModel.from_pretrained(self.pretrained_path+'model', config=self.config)
        self.model.to(self.device)
        self.model.eval()

    def generate_latex(self, img_path: str):
        '''
        Description:
            Generate latex sequence from the image by fine-tuned donut model.
        Parameter:
            img_path: input image file path
        Return:
            latex_output: latex output result
        '''
        length = 0
        limit = 0
        
        # easyOCR을 바탕으로 대략적인 길이를 추출
        result = self.reader.readtext(str(img_path), detail=0, allowlist=None, blocklist=None, width_ths=0.1,
                        height_ths=0.1, text_threshold=0.7, low_text=0.3,
                        link_threshold=0.1, canvas_size=2560, mag_ratio=1.5, slope_ths=0.2,
                        ycenter_ths=0.5, add_margin=0.1, output_format='dict')
    
        for i in result:
            for j in i:
                if isinstance(j, str):
                    length += len(j)
        
        length *=  2
        
        if length < 5:
            length = 5
        
        sample_test_img = Image.open(img_path).convert("RGB")
        sample_test_img = sample_test_img.resize((CFG.image_width, CFG.image_height))

        pixel_values = self.processor(sample_test_img, random_padding=True).pixel_values
        pixel_values = torch.FloatTensor(pixel_values).to(self.device)
        
        decoder_input_ids = torch.full(
            (1, 1),
            self.model.config.decoder_start_token_id,
            device=self.device,
        )
        
        # 추출 후 대략적인 길이로 먼저 sequence를 생성한다.
        outputs = self.model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=length,
            early_stopping=True,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
            top_k=1,
            bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )
        
        # <len> </len> 토큰 사이의 길이를 추출하기 위한 작업 > 줄 길이를 바탕으로 텍스트 길이를 계산한다.
        tmp = self.processor.tokenizer.batch_decode(outputs.sequences)[0].replace(' ','')[:34]
        print(tmp)
        Line_no = 1
        try:
            Line_no = int(re.findall(r'\d+', tmp)[0])
        except:
            Line_no = 1
        print(f'{Line_no}줄 짜리 텍스트입니다.')
        
        length //=  2
        
        print('\n latex 문을 출력중입니다...\n')
        while True:
            length = int(length * 1.02)
            Line = 0
            outputs = self.model.generate(
                pixel_values,
                decoder_input_ids=decoder_input_ids,
                max_length=length,
                early_stopping=True,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True,
                num_beams=1,
                top_k=1,
                bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
            )
            x = self.processor.tokenizer.batch_decode(outputs.sequences)[0]

            for i, j in enumerate(x):
                if x[i:i+4] == 'line':
                    Line += 1

            if Line >= Line_no * 2:
                break

            elif limit >= 50:
                break
            else:
                if int(length * 0.02) <= 1:
                    length += 1
                limit += 1

        # 최종 길이를 바탕으로 sequence 추출
        outputs = self.model.generate(
                pixel_values,
                decoder_input_ids=decoder_input_ids,
                max_length=length,
                early_stopping=True,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True,
                num_beams=1,
                top_k=1,
                bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
        )
        latex_output = self.processor.tokenizer.batch_decode(outputs.sequences)[0]

        return latex_output

    def post_process(self, output):
        '''
        Description:
            Post-process the outputs to sequence with latex.
        Parameter:
            output: result of the .generate_latex()
        Return:
            output: post_processed output
        '''
        if '<one>' in output:
            output = output.replace('<one>', '1')

        output = output.replace('<TPT><TPT>', '').replace('</s>', '').replace('</line>', '\n').replace('<line>', '').replace('<print>', '').replace('<hand>', '')
        output = re.sub(r"<len>.*?</len>", "", output)
        output = output.replace('<latex>', '$ ').replace('</latex>', ' $')
        # output = text_to_json(output)
        return output




## Sub 모델 파트 입니다
class BERT:
    '''
    Description:
        BERT Class for prediction.
    Parameter:
        pretrained_path: pretrained_path of the bert model. The path must contain model, tokenizer.
    Return:
        None
    '''
    def __init__(self, pretrained_path: str):
        self.MAX_LEN = 512
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path+'-tokenizer')
        self.model = BertForSequenceClassification.from_pretrained(pretrained_path)
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model = self.model.to(self.device)
        self.model.eval()

    def seqs2input(self, seqs: list):
        '''
        Description:
            Makes sequences to input format, input_ids and attention masks.
        Parameter:
            seqs: list of sequences. The number of sequences must be capable to our GPU Memory
        Return:
            input_ids: torch tensor (long) type
            attention_masks: torch tensor(long) type
        '''
        seq_bert = ['[CLS] ' + str(seq) + ' [SEP]' for seq in seqs]
        tokenized_texts = [self.tokenizer.tokenize(seq) for seq in seq_bert]

        input_ids = [self.tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
        input_ids = pad_sequences(input_ids, maxlen=self.MAX_LEN, dtype='long', truncating='post', padding='post')

        attention_masks = []

        for seq in input_ids:
            seq_mask = [float(i>0) for i in seq]
            attention_masks.append(seq_mask)

        return torch.tensor(input_ids), torch.tensor(attention_masks)

    def id2label(self, id):
        '''
        Description:
            Change the class id to Korean label.
        Parameter:
            id: label id
        Return:
            label: Korean label
        '''
        label = self.model.config.id2label[id]
        label = LABEL_TO_KR[label[0]] + label[1]
        return label

    def predict_sequences(self, seqs: list):
        '''
        Description:
            Predict sequences' label by BERT.
        Parameter:
            seqs: list of sequences. The number of sequences must be capable to our GPU Memory
        Return:
            kr_label: Korean labels of sequences
        '''
        input_ids, attention_masks = self.seqs2input(seqs)
        input_ids = input_ids.to(self.device)
        attention_masks = attention_masks.to(self.device)

        with torch.no_grad():
            pred = self.model(
                input_ids,
                token_type_ids=None,
                attention_mask=attention_masks
            )
        
        pred_np = pred[0].cpu().numpy()
        pred_label = np.argmax(pred_np, axis=1)
        kr_label = self.id2label(pred_label.item())

        return kr_label


def text_to_json(text):
    json_result = {
        "text": text
    }
    return json.dumps(json_result)