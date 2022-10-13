from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS

from utils.db import db
from utils.ma import ma


from resources.resources_1 import (
    GetEmailTemplate,
    GetEmailTemplateVersion,
    GetEmailTransactions,
    SendEmail,
)


app = Flask(__name__)

app.config.from_pyfile("config.py")
CORS(app)
api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)


api.add_resource(GetEmailTemplate, "/getemailtemplate")
api.add_resource(GetEmailTemplateVersion, "/getemailversion")
api.add_resource(GetEmailTransactions, "/getemailtransaction")
api.add_resource(SendEmail, "/sendemail")
