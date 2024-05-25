import os
import requests
import json


def handle_event(data):
    if "challenge" in data:
        return data["challenge"], 200

    if "event" in data:
        if "type" in data["event"]:
            if data["event"]["type"] != "message":
                return "", 200

    event = data["event"]

    # Don't respond to the bot's own messages, otherwise recursion
    if "bot_id" in event:
        if event["bot_id"] == "B074RSXM84U":
            return "", 200

    # Don't do anything if the message has been deleted or changed
    if "subtype" in event:
        if event["subtype"] != "bot_message":
            return "", 200

    # Don't do anything if the message is in a thread
    if "thread_ts" in event:
        return "", 200

    # Assume we're dealing with a new message & post a threaded reply
    event_ts = event["event_ts"]
    channel = event["channel"]

    # TODO: Based on the channelID, we want to customize the message

    slack_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    bearer_token = "Bearer " + slack_oauth_token

    # Define the URL and headers
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    payload = {
        "channel": channel,
        "thread_ts": event_ts,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here is a button:"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Click Me"
                        },
                        "value": "click_me_button",
                        "action_id": "button_click"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.json())

    return "", 200
