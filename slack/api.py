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


def slack_send_message(channel, thread_ts, text):
    slack_api('https://slack.com/api/chat.postMessage', {
        "channel": channel,
        "thread_ts": thread_ts,
        "blocks": [
            {
                "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": text
                        }
            }
        ]
    })


def slack_open_model(trigger_id, blocks, callback_id):
    slack_api('https://slack.com/api/views.open', {
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
            "blocks": blocks,
            "callback_id": callback_id
        }
    })


def slack_fallback_message(channel, thread_ts, elements, text):
    data = {
        "channel": channel,
        "blocks": [
            {
                "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": text
                        }
            },
            {
                "type": "actions",
                        "elements": elements
            }
        ]
    }

    if thread_ts is not None:
        data["thread_ts"] = thread_ts

    slack_api('https://slack.com/api/chat.postMessage', data)
