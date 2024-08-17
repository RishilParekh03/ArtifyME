from base import db
from base.com.vo.login_vo import LoginVO
from datetime import datetime


class UploadVO(db.Model):
    __tablename__ = 'artifyme_user_upload'

    upload_id = db.Column('upload_id', db.Integer, primary_key=True, autoincrement=True)
    original_filename = db.Column('original_filename', db.String(800), nullable=False)
    original_path = db.Column('original_path', db.String(800), nullable=False)
    stored_filename = db.Column('stored_filename', db.String(800), nullable=False)
    stored_path = db.Column('stored_path', db.String(800), nullable=False)
    upload_date = db.Column('upload_date', db.DateTime, default=datetime.utcnow().date(), nullable=False)
    upload_user_id = db.Column('upload_user_id', db.Integer,
                               db.ForeignKey(LoginVO.user_id, onupdate='CASCADE', ondelete='CASCADE'),
                               nullable=False)

    def as_dict(self):
        return {
            'upload_id': self.upload_id,
            'original_filename': self.original_filename,
            'original_path': self.original_path,
            'stored_filename': self.stored_filename,
            'stored_path': self.stored_path,
            'upload_date': self.upload_date,
            'upload_user_id': self.upload_user_id
        }


db.create_all()
