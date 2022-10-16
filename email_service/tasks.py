from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv(".env")

app = Celery(
    backend=os.getenv("REDIS_BACKEND_BROKER"),
    broker=os.getenv("REDIS_BACKEND_BROKER"),
    singleton_backend_url=os.getenv("REDIS_BACKEND_BROKER"),
)


@app.task
def send_batch_emails(emails_and_models, template_id, from_email, tag, batch_id):
    pass


@app.task
def send_email(template_id, template_model, from_email, to_email, tag):
    pass
