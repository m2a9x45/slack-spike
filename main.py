import os
import requests
import json

from flask import Flask, request
from dotenv import load_dotenv

from slack.view_submission import view_submission

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"


# Guide on what payload shortcut payload look like:
# https://api.slack.com/reference/interaction-payloads/shortcuts
@app.route('/slack', methods=['POST'])
def handle_slack():
    # print("Form Data:", request.form["payload"])
    # Parse the payload as JSON
    data = json.loads(request.form["payload"])
    # Print the parsed JSON data
    # print("Parsed Data:", data)

    if data["type"] == "view_submission":
        form_submissions = view_submission(data)
        print(form_submissions)
        return "", 200

    slack_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    bearer_token = "Bearer " + slack_oauth_token

    # Define the URL and headers
    url = 'https://slack.com/api/views.open'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    triggerID = data["trigger_id"]
    print("Trigger ID:", triggerID)

    payload = {
        "trigger_id": triggerID,
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

    # Print the response from the server
    print(response.status_code)

    # If we want to update the view, we'll need to store the viewID
    print(response.json())

    return data, 200


if __name__ == '__main__':
    app.run(debug=True)
