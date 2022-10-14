from flask_restful import Resource
from flask import request
from resources.postmark.api import send_email
from marshmallow import Schema, fields, ValidationError


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
            return {"msg": "request is not the right schema", "details": e.messages}

        try:
            response = send_email(**request_json)
            return response, 202
        except Exception as e:
            return {"msg": "error when sending email", "details": str(e)}, 500
