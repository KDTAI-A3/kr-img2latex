<div align="center">
    <a href="https://github.com/KDTAI-A3/kr-img2latex">
          <img width="300" height="150" src="https://github.com/KDTAI-A3/kr-img2latex/assets/79557712/690e1566-d208-4135-b727-7dd3be0137b2">
    </a>
<div align="center">
    <a href="https://github.com/KDTAI-A3/kr-img2latex">
          <img width="600" height="350" src="https://github.com/KDTAI-A3/kr-img2latex/assets/79557712/c36352d6-04d7-4bb9-9589-9e167cae0bcd">
    </a>
    <br>
    <h1>KR-IMG2LATEX</h1>
    <p>
        Extract text with LaTeX from image in English and Korean
    </p>
    <p>
        Using DONUT, BERT and ChatGPT.
    </p>
    <h1></h1>
    <br>


## **DONUT FINE-TUNED MODEL**
![웹 캡처_27-7-2023_23146_](https://github.com/KDTAI-A3/kr-img2latex/assets/81287077/32bf89d0-98ff-4646-aa9b-7f74e862863a)

## **BERT FINE-TUNED MODEL**
![image](https://github.com/KDTAI-A3/kr-img2latex/assets/81287077/078accc2-a085-429b-abd3-84be864c960b)


## **Summary(Our Function)**
 수식이 포함된 이미지를 텍스트 및 Latex 형태로 변환 (한국어 지원, 손글씨 지원)  
 텍스트 및 Latex 변환 결과물을 바탕으로 `ChatGPT-API`를 통해 해당 수식의 다양한 정보 제공  
 해당 수식의 수준 분류 (초4 ~ 고3)  

## Team A3 - Caffeine-Holic
<img width="300" height="200" src="https://github.com/KDTAI-A3/kr-img2latex/assets/81287077/e46a6a13-6396-4973-8dc8-230a2812ca47">

 전현욱 : 팀장, 프로젝트 관리  
 왕준호 : 부팀장, Main Model 개발, 데이터 전처리  
 박동수 : Main Model 개발, 학습 전략 구성  
 장유림 : 서브 모델 개발, 데이터 전처리  
 박재현 : 서브 모델 개발, ChatGPT-API 기능 구현  
 박영규 : 서버 관리, 백엔드 개발, 모델 개발 보조  
 송승헌 : 서버 관리, 프론트엔드 개발, 모델 개발 보조  

## Our Model Score
 #### DONUT  
   F1 : 94.2%  
     Print Type : 98.9%  
     HandWritten Type : 92.6%  
   Levenshtein : 92.7%  
 #### BERT  
   Accuracy: 95%  

## Model Building Process
![image](https://github.com/KDTAI-A3/kr-img2latex/assets/81287077/1625d2a8-83b6-4ab3-9d32-d8f4171e72cf)

## Training Data
 출처: [AIHub 수식, 도형, 낙서기호 OCR 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=479)
 Token Vocabulary 출처: Notepad++ - Latex AutoComplete XML File

## References
 [DONUT(naver/clova)](https://github.com/clovaai/donut)
 [bert(Google/research)](https://github.com/google-research/bert)
 [kykim/bert-kor-base](https://github.com/kiyoungkim1/LMkor)
 [openai-api](https://openai.com/)
 [easyocr](https://github.com/JaidedAI/EasyOCR)
 [kaggle](https://www.kaggle.com/code/nbroad/donut-train-benetech)
</div>
