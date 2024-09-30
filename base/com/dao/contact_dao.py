from base import db


class ContactDAO:
    def insert_inquiry(self, contact_vo):
        db.session.add(contact_vo)
        db.session.commit()
