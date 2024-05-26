import os
import json
import requests

from slack.api import slack_api


# TODO: Update the message that the block action is coming from to disable the button
# Can maybe use the `chat.update` API?
def block_actions(data):
    if "actions" not in data:
        return

    action_id = data["actions"][0]["action_id"]

    # TODO: Check what we want to do with the block action, i.e. what's the next step in the workflow
    messages = {
        "button_click_unique_1": {
            "button_click_unique_4": "Consent approval screen not showing account",
            "button_click_unique_5": "Consent approval screen not showing account",
            "button_click_unique_6": "Consent approval screen not showing account",
        },
        "button_click_unique_2": {
            "button_click_unique_5": "Something something easy transfer",
            "type": "modal"
        },
        "button_click_unique_3": {
            "text": "Connected mortgages are owned by a different team",
            "type": "text"
        },
        "button_click_unique_4": {
            "button_click_unique_7": "Something else thing"
        }
    }

    if action_id not in messages:
        print("Unsupported action_id:", action_id)
        return

    thread_ts = data["container"]["thread_ts"]
    channel = data["container"]["channel_id"]

    reply_type = ""
    for key, value in messages[action_id].items():
        if key == "type":
            reply_type = value

    match reply_type:
        case "text":
            slack_api('https://slack.com/api/chat.postMessage', {
                "channel": channel,
                "thread_ts": thread_ts,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": messages[action_id]["text"]
                        }
                    }
                ]
            })
            return
        case "modal":
            trigger_id = data["trigger_id"]
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
            })
            return
        case _:
            elements = []
            for key, value in messages[action_id].items():
                elements.append({
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": value,
                    },
                    "value": "button_tap_connected_accounts",
                    "action_id": key
                })

            slack_api('https://slack.com/api/chat.postMessage', {
                "channel": channel,
                "thread_ts": thread_ts,
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
