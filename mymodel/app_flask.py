from flask import Flask, request, json
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from matplotlib import pyplot as plt
from torchvision.models import efficientnet_v2_s
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

is_cuda = torch.cuda.is_available()
device = torch.device('cuda' if is_cuda else 'cpu')

print('Current cuda device is', device)



model = efficientnet_v2_s(weights='IMAGENET1K_V1')
model.to(device)

with open('imagenet_class_index.json') as img_idxs:
    data_class_file=json.load(img_idxs)

data_class = dict(zip(map(lambda x:int(x),data_class_file.keys()),data_class_file.values()))

@app.route("/predict", methods=["POST"])
def predict():

    if request.method=='POST':
        f=request.files['file']

        fn = './uploads/' + secure_filename(f.filename)
        f.save(fn)

        image = np.array(cv2.imread(fn),dtype=float)
        print(image.shape)
        image =np.expand_dims(image.transpose(2,0,1),axis=0)

        tensor = torch.from_numpy(image).type(torch.FloatTensor)

        # model inference [2 LINES]
        model_input = tensor.to(device)
        predictions = model(model_input).cpu()
    

    # response
    result = predictions.detach().numpy()
    result = data_class[np.argmax(result)]

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
