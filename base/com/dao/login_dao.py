from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:
    def insert_user(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def search_user(self, login_vo):
        search_profile = LoginVO.query.filter_by(username=login_vo.username).first()
        return search_profile

    def edit_user(self, login_vo):
        search_profile = LoginVO.query.filter_by(user_id=login_vo.user_id).first()
        return search_profile
