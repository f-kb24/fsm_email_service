from re import L
from flask_restful import Resource
from flask import request
from resources.postmark.api import get_all_templates
from marshmallow import Schema, fields, ValidationError
from tasks import send_batch_emails, send_email
from models.schemas import BatchSchema


class GetAllTemplates(Resource):
    @classmethod
    def post(cls):
        try:
            response = get_all_templates()
        except Exception as e:
            return {"msg": str(e)}, 400
        return response, 200


class SendEmailRequestSchema(Schema):
    template_id = fields.Int()
    template_model = fields.Raw(required=True)
    from_email = fields.Str()
    to_email = fields.Str()
    tag = fields.Str()


class SendEmail(Resource):
    @classmethod
    def post(cls):
        request_json = request.get_json()
        try:
            SendEmailRequestSchema().load(request_json)
        except ValidationError as e:
            return {
                "msg": "request is not the right schema",
                "details": e.messages,
            }, 400

        try:
            # send_email.apply_async(
            #     args=[
            #         request_json["template_id"],
            #         request_json["template_model"],
            #         request_json["from_email"],
            #         request_json["to_email"],
            #         request_json["tag"],
            #     ]
            # )
            return {"msg": "email is now being sent"}, 200
        except Exception as e:
            return {"msg": "error when sending email", "details": str(e)}, 500


class EmailAndModelsSchema(Schema):
    email = fields.Str()
    template_model = fields.Raw(required=True)


class SendBatchRequestSchema(Schema):
    from_email = fields.Str()
    tag = fields.Str()
    template_id = fields.Int()
    emails_and_models = fields.Nested(EmailAndModelsSchema, many=True)


# EXAMPLE REQUEST BODY
# {
# 	"from_email": "about@fsmfrancis.com",
# 	"tag": "Invoice",
# 	"template_id": "29480074",
# 	"emails_and_models":[
#    {
#       "email":"francis@fty.gg",
#       "template_model":{
#          "name":"Francis",
#          "total":241.42,
#          "due_date":"2022-10-14",
#          "invoice_id":1234,
#          "date":"2022-08-04"
#       }
#    },
#    {
#       "email":"francis@fsmfrancis.com",
#       "template_model":{
#          "name":"FooBar",
#          "total":100.00,
#          "due_date":"2022-11-11",
#          "invoice_id":12356,
#          "date":"2022-08-02"
#       }
#    }
# 	]
# }


class SendBatch(Resource):
    @classmethod
    def post(cls):
        request_json = request.get_json()
        try:
            SendBatchRequestSchema().load(request_json)
        except ValidationError as e:
            return {"msg": "request is not the right schema", "details": e.messages}

        try:
            new_batch = BatchSchema().load(
                {
                    "list_of_emails": [
                        x["email"] for x in request_json["emails_and_models"]
                    ],
                    "template_id": request_json["template_id"],
                }
            )
            new_batch.save_to_db()
        except Exception as e:
            return {"msg": "error when inserting new batch", "details": str(e)}, 500
        try:
            send_batch_emails.apply_async(
                args=[
                    request_json["emails_and_models"],
                    new_batch.template_id,
                    "about@fsmfrancis.com",
                    request_json["tag"],
                    new_batch.id,
                ]
            )
            return {"msg": "batch is now being sent"}, 202
        except Exception as e:
            return {"msg": "error when sending batch email", "details": str(e)}, 500
