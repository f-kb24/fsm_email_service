from flask_restful import Resource
from flask import request
from models.email_template import EmailTemplateModel
from models.email_template_versions import EmailTemplateVersionModel
from models.email_transactions import EmailTransactions
from resources.postmark_api import send_email


class GetEmailTemplate(Resource):
    @classmethod
    def get(cls):
        template = EmailTemplateModel.find_by_id(1)
        if not template:
            return {"msg": "template not found"}, 404
        return {"msg": "template found"}, 200


class GetEmailTemplateVersion(Resource):
    @classmethod
    def get(cls):
        version = EmailTemplateVersionModel.find_by_id(1)
        if not version:
            return {"msg": "version not found"}, 404
        return {"msg": "version found"}, 200


class GetEmailTransactions(Resource):
    @classmethod
    def get(cls):
        transaction = EmailTransactions.find_by_id(1)
        if not transaction:
            return {"msg": "transaction not found"}, 404
        return {"msg": "transaction found"}, 200


class SendEmail(Resource):
    @classmethod
    def post(cls):
        request_json = request.get_json()

        try:
            send_email()
        except Exception as e:
            return {"msg": str(e)}, 500
        return {"msg": "email has been sent"}, 202
