from celery import Celery
import os
import psycopg2
import requests
from requests.exceptions import RequestException

app = Celery(
    backend=os.getenv("REDIS_BACKEND_BROKER"),
    broker=os.getenv("REDIS_BACKEND_BROKER"),
    singleton_backend_url=os.getenv("REDIS_BACKEND_BROKER"),
)


def connect_to_db():
    con = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        database=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_AUTH"),
    )
    return con


@app.task()
def send_email(postmark_template_id, send_to):
    body = {
        "TemplateId": postmark_template_id,
        "TemplateModel": {
            "product_name": "fsmfrancis",
            "name": "francis",
            "login_url": "http://google.com",
            "username": "fsmfrancis",
            "sender_name": "francis",
            "action_url": "http://google.com",
        },
        "InlineCss": True,
        "From": "about@fsmfrancis.com",
        "To": send_to,
        "Tag": "Invitation",
        "TrackOpens": True,
        "TrackLinks": "None",
    }
    try:
        response = requests.post(
            "https://api.postmarkapp.com/email/withTemplate",
            headers={
                "Accept": "application/json",
                "X-Postmark-Server-Token": os.getenv("POSTMARK_API_TOKEN"),
            },
            json=body,
        )

        # if http status code 400-500 -> raise an exception
        response.raise_for_status()

        # response has a MessageID that needs to be saved into db
    except RequestException as e:
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        raise Exception(f"General Error: {str(e)}")
