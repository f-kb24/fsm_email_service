import os
from dotenv import load_dotenv

load_dotenv(".env")

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_RUN_PORT = os.getenv("FLASK_RUN_PORT")
# JWT_SECRET_KEY = os.getenv("SECRET_KEY")
# CORS_EXPOSE_HEADERS = ["tokens", "Set-Cookie"]
# CORS_SUPPORTS_CREDENTIALS = True

CORS_EXPOSE_HEADERS = [
    "tokens",
    "Set-Cookie",
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Credentials",
]
CORS_SUPPORTS_CREDENTIALS = True


# DEV
# SQLALCHEMY_ECHO = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
