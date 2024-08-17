from base import db
from datetime import datetime


class LoginVO(db.Model):
    __tablename__ = 'artifyme_user_data'

    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(50), unique=True, nullable=False)
    username = db.Column('email', db.String(50), unique=True, nullable=False)
    password = db.Column('password', db.String(60), nullable=False)
    reg_date = db.Column('reg_date', db.DateTime, default=datetime.utcnow().date(), nullable=False)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'reg_date': self.reg_date
        }


db.create_all()
