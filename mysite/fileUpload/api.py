
import json
from uuid import uuid4
from django.utils import timezone
import requests

from django.conf import settings

import base64

def sendImageAPI(file, api_key = settings.API_KEY, request_id = uuid4(), timestamp = timezone.now()):
    file_data = base64.b64encode(file.read()).decode('utf-8')
    API_settings = ('SendImage/sendimage','file','img_num')
    return commonAPI(API_settings,file_data,api_key,request_id,timestamp)


def commonAPI(API_settings, data, api_key = settings.API_KEY, request_id = uuid4(), timestamp = timezone.now()):
    API_url, data_name, result_name = API_settings
    post_data = {
            'api-key':api_key,
            'request_id': str(request_id),
            'timestamp': str(timestamp) ,
            data_name : data,
        }
    #post_data = (post_data.items())
    response = requests.post(settings.SERVER_URL+API_url,  
        json = post_data
        )
    print(response.content)
    if response.status_code == 200:
        
        response_data = json.loads(response.content)
        if(response_data['is_success']):
            return (True,response_data[result_name],response_data['timestamp'])
    return (False, f"ERROR: NO_RESULT{ response.status_code}","ERROR")


def imgToLatexAPI(img_num, api_key = settings.API_KEY, request_id = uuid4(), timestamp = timezone.now()):
     API_settings = ('/Img2Latex/img2latex','img_num','result')
     return commonAPI(API_settings,img_num,api_key,request_id,timestamp)
     
def classifyLatexAPI(img_num, api_key = settings.API_KEY, request_id = uuid4(), timestamp = timezone.now()):
     API_settings = ('/CLF_LATEX/clf-latex','img_num','result')
     return commonAPI(API_settings,img_num,api_key,request_id,timestamp)