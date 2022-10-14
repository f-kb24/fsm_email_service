from utils.db import db
from utils.ma import ma
from datetime import datetime
from models.postmark_template import PostmarkTemplateSchema


class PostmarkTemplateVersionModel(db.Model):
    __tablename__ = "pm_template_version"

    postmark_template_id = db.Column(db.Integer(), primary_key=True)
    postmark_template_alias = db.Column(db.String())
    postmark_template_subject = db.Column(db.String())
    postmark_template_htmlbody = db.Column(db.String())
    postmark_template_textbody = db.Column(db.String())
    postmark_template_type = db.Column(db.String())
    postmark_layout_template = db.Column(db.String())

    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    template_name = db.Column(db.String(120), db.ForeignKey("pm_templates.name"))

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


class PostmarkTemplateVersionSchema(ma.SQLAlchemyAutoSchema):
    template = ma.Nested(PostmarkTemplateSchema)

    class Meta:
        sqla_session = db.session
        model = PostmarkTemplateVersionModel
        load_instance = True
        include_fk = True


pm_template_version_schema = PostmarkTemplateVersionSchema()
