import requests
import os
from requests.exceptions import RequestException


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


def send_email(template_id, template_model, from_email, to_email, tag):
    body = {
        "TemplateId": template_id,
        "TemplateModel": template_model,
        "InlineCss": True,
        "From": f"FSM Francis <{from_email}>",
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
