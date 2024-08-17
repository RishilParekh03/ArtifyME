from base import db


# from base.com.vo.contact_vo import ContactVO


class ContactDAO:
    def insert_inquiry(self, contact_vo):
        db.session.add(contact_vo)
        db.session.commit()
