from utils.db import db
from datetime import datetime
from sqlalchemy.types import ARRAY


class TemplateModel(db.Model):
    __tablename__ = "templates"

    id = db.Column(db.Integer(), primary_key=True)
    alias = db.Column(db.String())
    name = db.Column(db.String())
    info = db.Column(db.JSON())

    batches = db.relationship("BatchModel", backref="template")
    email_transactions = db.relationship("EmailTransactionModel", backref="template")

    @classmethod
    def find_by_id(cls, _id):
        result = cls.query.filter_by(id=_id).first()
        return result

    @classmethod
    def find_all_by_name(cls, name):
        result = cls.query.filter_by(name=name).all()
        return result

    @classmethod
    def find_all(cls):
        result = cls.query.filter(TemplateModel.name != "Basic").all()
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class EmailTransactionModel(db.Model):
    __tablename__ = "email_transactions"

    postmark_message_id = db.Column(db.String(), primary_key=True)
    sent_to = db.Column(db.String(120), nullable=False)
    date_sent = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)
    email_opened = db.Column(db.Boolean(), default=False)
    email_clicked = db.Column(db.Boolean(), default=False)

    batch_id = db.Column(db.Integer(), db.ForeignKey("batches.id"))
    template_id = db.Column(db.Integer(), db.ForeignKey("templates.id"))

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


class BatchModel(db.Model):
    __tablename__ = "batches"

    id = db.Column(db.Integer, primary_key=True)
    list_of_emails = db.Column(ARRAY(db.String()))
    date_sent = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)

    email_transactions = db.relationship("EmailTransactionModel", backref="batch")
    template_id = db.Column(db.Integer(), db.ForeignKey("templates.id"))

    @classmethod
    def find_by_id(cls, _id):
        result = cls.query.filter_by(id=_id).first()
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
