from celery import Celery
import os
from requests.exceptions import RequestException

app = Celery(
    backend=os.getenv("REDIS_BACKEND_BROKER"),
    broker=os.getenv("REDIS_BACKEND_BROKER"),
    singleton_backend_url=os.getenv("REDIS_BACKEND_BROKER"),
)


@app.task()
def send_email(postmark_template_id, address_to_send):
    pass
