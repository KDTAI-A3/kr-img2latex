from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from models import db, ImgFiles, ExtractedResult, ClfResult

from logs import log_write

import os
import datetime
import base64

API_KEY = 'CAFFEINE-HOLIC'

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(base_dir, 'db.sqlite')

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

    db.init_app(app)
    db.app = app
    db.create_all()

api = Api(app, 
          version='0.9',
          title='AI-Server-API',
          description='AI-Server API 문서',
          doc='/api-docs')

sendimage_api = api.namespace('SendImage',
                             description='이미지를 서버로 전송하는 api')

sendimage_fields = sendimage_api.model('SendImageModel', {
    'api-key': fields.String(description='api-key'),
    'request_id':fields.String(description='request uuid4 string'),
    'timestamp':fields.DateTime(description='datetime field'),
    'file':fields.String(description='Image file content as base64 encoded string')
})

@sendimage_api.route('/sendimage')
class SendImage(Resource):
    @sendimage_api.expect(sendimage_fields)
    def post(self):
        data = sendimage_api.payload

        if data['api-key'] != API_KEY:
            return {
                'is_success': False,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'img_num': -1,
                }

        try:
            new_img = ImgFiles()
            db.session.add(new_img)
            db.session.commit()

            image_data = data['file']
            file_path = f'./img_files/image_{new_img.img_num}.png'

            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(image_data))

            creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_img.img_file_path = file_path
            new_img.created_time = creation_time

            result_dict = {
                'is_success': True,
                'timestamp': creation_time,
                'img_num': new_img.img_num,
            }
            
            log_write('SendImage API SUCCESS')

            return result_dict
        except Exception as err:
            log_write('SendImage API FAILED, Detail: '+err)

            return {
                'is_success': False,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'img_num': -2,
            }

img2latex_api = api.namespace('Img2Latex',
                             description='이미지를 텍스트 및 latex 문법으로 변환해주는 API')

img2latex_fields = img2latex_api.model('Img2LatexModel', {
    'api-key': fields.String(description='api-key'),
    'request_id':fields.String(description='request uuid4 string'),
    'timestamp':fields.DateTime(description='datetime field'),
    'img_num':fields.Integer(description='Image Number')
})

@img2latex_api.route('/img2latex')
class Img2Latex(Resource):
    @img2latex_api.expect(img2latex_fields)
    def post(self):
        data = img2latex_api.payload

        if data['api-key'] != API_KEY:
            return {
                'is_success': False,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'result': -1,
                }

        new_text_result = ExtractedResult()

        try:
            img_file_path = f'./img_files/image_{data["img_num"]}.png'
            
            ### MODEL WILL PARSE THE IMAGE
            # model.generate(...)
            
            extracted_text = "Model Result will be here"
            creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_text_result.img_num = data['img_num']
            new_text_result.is_success = True
            new_text_result.result = extracted_text

            db.session.add(new_text_result)
            db.session.commit()

            log_write('Img2Latex API SUCCESS')

            result_dict = {
                    'is_success': True,
                    'timestamp': creation_time,
                    'result': extracted_text,
                }

            return result_dict
        
        except Exception as err:
            new_text_result.img_num = data['img_num']
            new_text_result.is_success = False
            new_text_result.result = None

            db.session.add(new_text_result)
            db.session.commit()

            log_write('Img2Latex API FAILED')

            return {
                    'is_success': False,
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'result': -2
                    }

clf_latex_api = api.namespace('CLF_LATEX',
                             description='텍스트 및 latex 문법을 수준별로 분류하는 API')

clf_latex_fields = clf_latex_api.model('ClF_LatexModel', {
    'api-key': fields.String(description='api-key'),
    'request_id':fields.String(description='request uuid4 string'),
    'timestamp':fields.DateTime(description='datetime field'),
    'img_num':fields.Integer(description='Image Number')
})

@clf_latex_api.route('/clf-latex')
class ClfLatex(Resource):
    @clf_latex_api.expect(clf_latex_fields)
    def post(self):
        data = clf_latex_api.payload

        if data['api-key'] != API_KEY:
            return {
                'is_success': False,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'result': -1,
                }

        new_clf_result = ClfResult()

        try:
            input_text = ExtractedResult.query.filter(ExtractedResult.img_num==data['img_num']).first()

            ### MODEL WILL PARSE THE IMAGE
            # model.generate(...)
            
            clf_result = "E2" # temp
            creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_clf_result.img_num = data['img_num']
            new_clf_result.is_success = True
            new_clf_result.result = clf_result

            db.session.add(new_clf_result)
            db.session.commit()

            log_write('ClfLatex API SUCCESS')

            result_dict = {
                    'is_success': True,
                    'timestamp': creation_time,
                    'result': clf_result,
                }
            
            return result_dict
        
        except Exception as err:
            new_clf_result.img_num = data['img_num']
            new_clf_result.is_success = False
            new_clf_result.result = None

            db.session.add(new_clf_result)
            db.session.commit()

            log_write('ClfLatex API FAILED')

            return {
                    'is_success': False,
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'result': -2
                    }


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)