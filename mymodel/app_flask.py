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
app = Flask(__name__)

# assign model handler as global variable [2 LINES]
is_cuda = torch.cuda.is_available()
device = torch.device('cuda' if is_cuda else 'cpu')

print('Current cuda device is', device)



model = efficientnet_v2_s(weights='IMAGENET1K_V1')
transforms_val = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@app.route("/predict", methods=["POST"])
def predict():

    if request.method=='POST':
        f=request.files['file']

        fn = f.filename
        f.save(fn)
        image = np.array(cv2.imread(fn),dtype=float)
        #image = cv2.resize(image,dsize=(10,10),interpolation=cv2.INTER_LINEAR)
        #image_swap = np.swapaxes(image, 0,2)
        #image_swap = np.expand_dims(image_swap, axis=0)
        tensor = torch.from_numpy(image).type(torch.FloatTensor)

        # model inference [2 LINES]
        model_input = tensor.to(device)
        predictions = model(model_input)
    

    # response
    result = json.dumps(predictions)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
