from utils.db import db
from datetime import datetime


class EmailTemplateVersionModel(db.Model):
    __tablename__ = "email_versions"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    description = db.Column(db.String(240))
    postmark_id = db.Column(db.Integer(), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey("email_templates.id"))

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
