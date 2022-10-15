from celery import Celery
import os
import psycopg2
import requests
from requests.exceptions import RequestException
from dateutil import parser
from dotenv import load_dotenv
import pusher

load_dotenv(".env")

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


def connect_to_pusher():
    pusher_client = pusher.Pusher(
        app_id=os.getenv("APP_ID"),
        key=os.getenv("KEY"),
        secret=os.getenv("SECRET"),
        cluster="us3",
        ssl=True,
    )
    return pusher_client


@app.task
def send_batch_emails(emails_and_models, template_id, from_email, tag, batch_id):
    # emails and models will have the schema:
    # {"email": "foo@example.com", "template_model": {"name": "foobar", ..etc}}

    messages = []

    for user_info in emails_and_models:
        messages.append(
            {
                "TemplateId": template_id,
                "TemplateModel": user_info["template_model"],
                "InlineCss": True,
                "From": f"FSM Email Demo <{from_email}>",
                "To": user_info["email"],
                "Tag": tag,
                "TrackOpens": True,
                "TrackLinks": "None",
            }
        )
    try:
        response = requests.post(
            "https://api.postmarkapp.com/email/batchWithTemplates",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Postmark-Server-Token": os.getenv("POSTMARK_API_TOKEN"),
            },
            json={"Messages": messages},
        )
        # if http status code 400-500 -> raise an exception
        response.raise_for_status()

        # this assumes there are no errors with postmark sending batch emails
        response_json = response.json()
    except RequestException as e:
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        raise Exception(f"General Error: {str(e)}")

    connection = connect_to_db()
    cursor = connection.cursor()

    for sent_email in response_json:
        # there may be individual errors with emails being sent
        # error handling would be done with logging
        try:
            cursor.execute(
                """
                    insert into email_transactions 
                    (postmark_message_id, sent_to, batch_id, template_id, date_sent, email_opened, email_clicked)
                    values (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    sent_email["MessageID"],
                    sent_email["To"],
                    batch_id,
                    template_id,
                    parser.parse(sent_email["SubmittedAt"]),
                    False,
                    False,
                ),
            )
            connection.commit()
        except Exception as e:
            print(e)
    # PUSHER
    connection.close()


@app.task
def send_email(template_id, template_model, from_email, to_email, tag):
    body = {
        "TemplateId": template_id,
        "TemplateModel": template_model,
        "InlineCss": True,
        "From": f"FSM Email Demo <{from_email}>",
        "To": to_email,
        "Tag": tag,
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
        response_json = response.json()

        pusher_client = connect_to_pusher()
        pusher_client.trigger(
            "fsmfrancis",
            "email_sent",
            {
                "msg": f'email to {response_json["To"]} has been sent. ID: {response_json["MessageID"]}'
            },
        )
    except RequestException as e:
        pusher_client = connect_to_pusher()
        pusher_client.trigger(
            "fsmfrancis",
            "email_sent",
            {"msg": f"ERROR: email failed - {str(e)} "},
        )
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        pusher_client = connect_to_pusher()
        pusher_client.trigger(
            "fsmfrancis",
            "email_sent",
            {"msg": f"ERROR: email failed - {str(e)} "},
        )
        raise Exception(f"General Error: {str(e)}")

    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
                insert into email_transactions 
                (postmark_message_id, sent_to, template_id, date_sent, email_opened, email_clicked)
                values (%s, %s, %s, %s, %s, %s)
            """,
            (
                response_json["MessageID"],
                response_json["To"],
                template_id,
                parser.parse(response_json["SubmittedAt"]),
                False,
                False,
            ),
        )
        connection.commit()
    except Exception as e:
        print(e)
    # PUSHER
    connection.close()


@app.task
def track_open(message_id):
    # this will hit the message open api with the message id
    pass
