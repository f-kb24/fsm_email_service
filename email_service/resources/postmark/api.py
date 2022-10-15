import requests
import os
from requests.exceptions import RequestException


def get_all_templates():
    try:
        # this assumes we have less than 100 templates
        # if more than 100 templates adjust count & offset
        response = requests.get(
            f"https://api.postmarkapp.com/templates?count=100&offset=0",
            headers={
                "Accept": "application/json",
                "X-Postmark-Server-Token": os.getenv("POSTMARK_API_TOKEN"),
            },
        )
        response.raise_for_status()

        return response.json()

    except RequestException as e:
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        raise Exception(f"General Error: {str(e)}")


def get_template(template_id):
    try:
        response = requests.get(
            f"https://api.postmarkapp.com/templates/{template_id}",
            headers={
                "Accept": "application/json",
                "X-Postmark-Server-Token": os.getenv("POSTMARK_API_TOKEN"),
            },
        )
        response.raise_for_status()

        return response.json()

    except RequestException as e:
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        raise Exception(f"General Error: {str(e)}")


def send_batch_emails(emails_and_models, template_id, from_email, tag):
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
        return response.json()

        # response has a MessageID that needs to be saved into db
    except RequestException as e:
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        raise Exception(f"General Error: {str(e)}")


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
        return response.json()

        # response has a MessageID that needs to be saved into db
    except RequestException as e:
        raise Exception(f"HTTP Error: {str(e)}")
    except Exception as e:
        raise Exception(f"General Error: {str(e)}")
