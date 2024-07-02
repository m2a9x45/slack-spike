import os
import requests

from flask import request


def handle_oauth_slack():
    data = request.json
    print(data)

    code = data["code"]

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    redirect_uri = os.getenv('SLACK_REDIRECT_URL')
    client_id = os.getenv('SLACK_CLIENT_ID')
    client_secret = os.getenv('SLACK_CLIENT_SECRET')

    payload = 'code=' + code + '&redirect_uri=' + redirect_uri + \
        '&client_id=' + client_id + '&client_secret=' + client_secret

    url = "https://slack.com/api/openid.connect.token"

    response = requests.post(url, headers=headers, data=payload)
    print("Slack API:", response.status_code, response.json())

    # Check if the response if successful

    # Check if the user already has an account
    # If so log them in, return a cookie / session
    # Else create a new user

    return "", 200
