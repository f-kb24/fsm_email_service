from flask_restful import Resource
from models.index import TemplateModel
from resources.postmark.api import get_template, get_all_templates
from models.schemas import TemplateSchema


class GetTemplates(Resource):
    @classmethod
    def get(cls):
        templates = TemplateModel.find_all()

        return TemplateSchema(many=True).dump(templates)


class SyncTemplates(Resource):
    @classmethod
    def post(cls):
        try:
            response = get_all_templates()
        except Exception as e:
            return {
                "msg": " something went wrong with getting all templates",
                "details": str(e),
            }, 500

        templates_that_were_loaded = []
        for template in response["Templates"]:
            template_in_db = TemplateModel.find_by_id(template["TemplateId"])

            if not template_in_db:
                try:
                    template_info = get_template(template["TemplateId"])
                    template_loaded = TemplateSchema().load(
                        {
                            "id": template["TemplateId"],
                            "alias": template["Alias"],
                            "name": template["Name"],
                            "info": template_info,
                        }
                    )
                    template_loaded.save_to_db()
                    templates_that_were_loaded.append(str(template["TemplateId"]))
                except Exception as e:
                    # if one template DNE, do not break loop
                    # realistically, there should be error logging
                    print(e)
                    pass
        if len(templates_that_were_loaded) == 0:
            return {"msg": "Database is already in sync with Postmark"}, 200
        template_id_joined_strings = ", ".join(templates_that_were_loaded)
        return {"msg": f"{template_id_joined_strings} were loaded into database"}, 200
