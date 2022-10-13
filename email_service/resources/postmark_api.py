import requests
import os
from requests.exceptions import RequestException


def send_email():
    body = {
        "TemplateId": 29462080,
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
        "To": "francis@fsmfrancis.com",
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
