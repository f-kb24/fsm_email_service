from utils.db import db
from datetime import datetime


class EmailTransactions(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    sent_to = db.Column(db.String(120), nullable=False)
    date_sent = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)
    email_opened = db.Column(db.Boolean(), default=False)
    email_clicked = db.Column(db.Boolean(), default=False)
    email_template_version = db.Column(db.Integer, db.ForeignKey("email_versions.id"))
    postmark_message_id = db.Column(db.String())

    @classmethod
    def find_by_id(cls, _id):
        result = cls.query.filter_by(id=_id).first()
        return result

    @classmethod
    def find_all_sent(cls, sent_to):
        result = cls.query.filter_by(sent_to=sent_to).all()
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
