from flask_restful import Resource
from flask import request
from models.postmark_template import PostmarkTemplateModel
from models.postmark_template_version import PostmarkTemplateVersionModel
from models.email_transactions import EmailTransactions
from resources.postmark.api import send_email


class GetEmailTemplate(Resource):
    @classmethod
    def get(cls):
        template = PostmarkTemplateModel.find_by_name("name")
        if not template:
            return {"msg": "template not found"}, 404
        return {"msg": "template found"}, 200


class GetEmailTemplateVersion(Resource):
    @classmethod
    def get(cls):
        version = PostmarkTemplateVersionModel.find_by_id(1)
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
        # {send_to, }
        try:
            send_email()
        except Exception as e:
            return {"msg": str(e)}, 500
        return {"msg": "email has been sent"}, 202
