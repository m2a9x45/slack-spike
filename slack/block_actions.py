import os
import json
import requests


# TODO: Update the message that the block action is coming from to disable the button
# Can maybe use the `chat.update` API?
def block_actions(data):
    if "actions" not in data:
        return

    action_id = data["actions"][0]["action_id"]

    messages = {
        "button_click_connected_accounts": {
            "text": "Consent approval screen not showing account",
            "action_id": "button_click_unique_1"
        },
        "button_click_easy_bank_transfer": {
            "text": "Something something easy transfer",
            "action_id": "button_click_unique_1"
        },
        "button_click_something_else": {
            "text": "Something else thing",
            "action_id": "button_click_unique_1"
        }
    }

    if action_id not in messages:
        print("Unsupported action_id:", action_id)
        return

    thread_ts = data["container"]["thread_ts"]
    channel = data["container"]["channel_id"]

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
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": messages[action_id]["text"],
                        },
                        "value": "button_tap_connected_accounts",
                        "action_id": messages[action_id]["action_id"]
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.json())
