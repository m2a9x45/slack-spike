import os
import requests
import json


def shortcut(data):
    slack_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    bearer_token = "Bearer " + slack_oauth_token

    # Define the URL and headers
    url = 'https://slack.com/api/views.open'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    trigger_id = data["trigger_id"]
    print("Trigger ID:", trigger_id)

    payload = {
        "trigger_id": trigger_id,
        "view": {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "My App",
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Thing",
                    }
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.json())
