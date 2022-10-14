from flask_restful import Resource
from flask import request
from models.postmark_template import PostmarkTemplateModel, pm_template_schema
from models.postmark_template_version import (
    PostmarkTemplateVersionModel,
    pm_template_version_schema,
)

# from models.email_template_versions import EmailTemplateVersionModel
# from models.email_transactions import EmailTransactions
from resources.postmark.api import send_email, get_template


class AddEmailTemplate(Resource):
    @classmethod
    def post(cls, postmark_template_id):
        try:
            # GET TEMPLATE RESPONSE SCHEMA
            # "Name": string,
            # "TemplateId": int,
            # "Alias": string,
            # "Subject": string,
            # "HtmlBody": string,
            # "TextBody": string
            # "AssociatedServerId": int
            # "Active": boolean
            # "TemplateType": string
            # "LayoutTemplate": string
            template_info = get_template(postmark_template_id)
        except Exception as e:
            return {"msg": str(e)}, 500
        template = PostmarkTemplateModel.find_by_name(template_info["Name"])
        # this assumes Postmark is consistent with their response schemas
        # otherwise schema validation would be necessary

        # if email template does not exist, add new email template
        # templates will be grouped by Name, because that's how postmark does it
        if not template:
            try:
                new_email_template = pm_template_schema.load(
                    {"name": template_info["Name"]}
                )
                new_email_template.save_to_db()
            except Exception as e:
                return {
                    "msg": "error when creating new template",
                    "description": str(e),
                }, 500

        # template = PostmarkTemplateModel.find_by_name(template_info["Name"])
        # add new template version based on template name
        try:
            new_template_version = pm_template_version_schema.load(
                {
                    "postmark_template_id": template_info["TemplateId"],
                    "postmark_template_alias": template_info["Alias"],
                    "postmark_template_subject": template_info["Subject"],
                    "postmark_template_htmlbody": template_info["HtmlBody"],
                    "postmark_template_textbody": template_info["TextBody"],
                    "postmark_template_type": template_info["TemplateType"],
                    "postmark_layout_template": template_info["LayoutTemplate"],
                    "template_name": template_info["Name"],
                }
            )
            new_template_version.save_to_db()
        except Exception as e:
            return {
                "msg": "error when creating new template version",
                "description": str(e),
            }, 500

        return {
            "msg": f"postmark template {template_info['Name']} ID: {template_info['TemplateId']} has been added"
        }, 201
