from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS

from utils.db import db
from utils.ma import ma


from resources.templates import SyncTemplates, GetTemplates
from resources.email_transactions import SendEmail, SendBatch, GetAllTemplates


app = Flask(__name__)

app.config.from_pyfile("config.py")
CORS(app)
api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)

api.add_resource(SendEmail, "/sendemail")
api.add_resource(SendBatch, "/sendbatch")
api.add_resource(SyncTemplates, "/synctemplates")
api.add_resource(GetTemplates, "/gettemplates")

# api.add_resource(AddEmailTemplate, "/addemailtemplate/<string:postmark_template_id>")
