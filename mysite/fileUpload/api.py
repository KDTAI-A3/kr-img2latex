
import json
from uuid import uuid4
from django.utils import timezone
import requests

SERVER_URL = "http://localhost:8080/" #http://ec2-52-59-253-171.eu-central-1.compute.amazonaws.com:8000/"
API_KEY = 'CAFFEINE-HOLIC'



def sendImageAPI(file, api_key = API_KEY, request_id = uuid4(), timestamp = timezone.now()):
    post_data = {
            'api-key': api_key,
            'request_id': str(request_id),
            'timestamp': str(timestamp) ,
            'file':file,
        }
    post_data = (post_data.items())
    response = requests.post(SERVER_URL+'sendimage',  
        files = post_data
        )
    if response.status_code == 200:
        print(response.content)
        response_data = json.loads(response.content)
        if(response_data['is_success']):
            return (True,response_data['img_num'],response_data['timestamp'])
    return (False, "ERROR","ERROR")



def commonAPI(API_url, img_num, api_key = API_KEY, request_id = uuid4(), timestamp = timezone.now()):
    post_data = {
            'api-key':api_key,
            'request_id': str(request_id),
            'timestamp': str(timestamp) ,
            'img_num':img_num,
        }
    post_data = (post_data.items())
    response = requests.post(SERVER_URL+API_url,  
        data = post_data
        )
    if response.status_code == 200:
        print(response.content)
        response_data = json.loads(response.content)
        if(response_data['is_success']):
            return (True,response_data['result'],response_data['timestamp'])
    return (False, "ERROR: NO_RESULT","ERROR")


def imgToLatexAPI(img_num, api_key = API_KEY, request_id = uuid4(), timestamp = timezone.now()):
     return commonAPI('img2latex',img_num,api_key,request_id,timestamp)
     
def classifyLatexAPI(img_num, api_key = API_KEY, request_id = uuid4(), timestamp = timezone.now()):
     return commonAPI('clf-latex',img_num,api_key,request_id,timestamp)