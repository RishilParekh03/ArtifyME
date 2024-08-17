from base import db
from base.com.vo.login_vo import LoginVO
from datetime import datetime


class ContactVO(db.Model):
    __tablename__ = 'artifyme_inquiry_data'

    inquiry_id = db.Column('inquiry_id', db.Integer, primary_key=True, autoincrement=True)
    feedback = db.Column('feedback', db.String(700), nullable=False)
    inquiry_date = db.Column('inquiry_date', db.DateTime, default=datetime.utcnow().date(), nullable=False)
    inquiry_user_id = db.Column('inquiry_user_id', db.Integer,
                                db.ForeignKey(LoginVO.user_id, ondelete='CASCADE', onupdate='CASCADE'),
                                nullable=False)
    inquiry_user_email = db.Column('inquiry_user_email', db.String(50), nullable=False)

    def as_dict(self):
        return {
            'inquiry_id': self.inquiry_id,
            'inquiry': self.feedback,
            'inquiry_date': self.inquiry_date,
            'inquiry_user_id': self.inquiry_user_id,
            'inquiry_user_email': self.inquiry_user_email
        }


db.create_all()
