import os
import json
import requests


def slack_api(url, payload):
    slack_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    bearer_token = "Bearer " + slack_oauth_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Slack API:", response.status_code, response.json())
