from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ImgFiles(db.Model):
    __tablename__ = 'imgfiles'

    img_num = db.Column('img_num', 
                        db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    img_file_path = db.Column('img_file_path',
                            db.String(255))
    created_time = db.Column('created_time',
                             db.String(64))
    
    db.relationship('extracted_result', 'clf_result')

class ExtractedResult(db.Model):
    __tablename__ = 'extracted_result'

    extract_num = db.Column('extract_num', 
                        db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    img_num = db.Column('img_num', 
                        db.Integer,
                        db.ForeignKey('imgfiles.img_num'))
    is_success = db.Column('is_success',
                           db.Boolean)
    result = db.Column('result',
                       db.String(255))
    
class ClfResult(db.Model):
    __tablename__ = 'clf_result'

    clf_num = db.Column('clf_num', 
                        db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    img_num = db.Column('img_num', 
                        db.Integer,
                        db.ForeignKey('imgfiles.img_num'),)
    is_success = db.Column('is_success',
                           db.Boolean)
    result = db.Column('result',
                       db.String(45))

