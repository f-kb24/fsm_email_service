from models.index import TemplateModel, EmailTransactionModel, BatchModel
from utils.ma import ma
from utils.db import db


class TemplateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TemplateModel
        load_instance = True
        include_fk = True
        sqla_session = db.session
        load_only = ("info",)


class BatchSchema(ma.SQLAlchemyAutoSchema):
    template = ma.Nested(TemplateSchema)

    class Meta:
        model = BatchModel
        load_instance = True
        include_fk = True
        sqla_session = db.session


class BatchSchemaWithoutNest(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BatchModel
        load_instance = True
        sqla_session = db.session


class EmailTransactionSchema(ma.SQLAlchemyAutoSchema):
    template = ma.Nested(TemplateSchema)
    batch = ma.Nested(BatchSchemaWithoutNest)

    class Meta:
        model = EmailTransactionModel
        load_instance = True
        include_fk = True
        sqla_session = db.session
