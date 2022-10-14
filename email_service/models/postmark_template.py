from utils.db import db
from utils.ma import ma
from datetime import datetime


class PostmarkTemplateModel(db.Model):
    __tablename__ = "pm_templates"
    name = db.Column(db.String(120), nullable=False, primary_key=True, unique=True)

    @classmethod
    def find_by_name(cls, name):
        result = cls.query.filter_by(name=name).first()
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class PostmarkTemplateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = PostmarkTemplateModel
        load_instance = True


pm_template_schema = PostmarkTemplateSchema()
