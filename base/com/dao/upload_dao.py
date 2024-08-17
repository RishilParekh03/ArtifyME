from base import db
from base.com.vo.upload_vo import UploadVO


class UploadDAO:
    def insert_image(self, upload_vo):
        db.session.add(upload_vo)
        db.session.commit()
