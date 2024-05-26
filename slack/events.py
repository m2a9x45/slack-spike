import os
import requests
import json

from slack.api import slack_api
from workflow.config import get_options


def handle_event(data):
    if "challenge" in data:
        return data["challenge"], 200

    if "event" in data:
        if "type" in data["event"]:
            if data["event"]["type"] != "message":
                return "", 200

    event = data["event"]
    event_ts = event["event_ts"]
    channel = event["channel"]

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
    elements = get_options()
    slack_api('https://slack.com/api/chat.postMessage', {
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
                "elements": elements
            }
        ]
    })

    return "", 200
