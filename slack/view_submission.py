import os
import requests
import json


# Handles model submissions, currently only supports the text input felid
# https://api.slack.com/surfaces/modals#interactions
def view_submission(data):
    blocks = data["view"]["blocks"]
    state = data["view"]["state"]["values"]

    # We want to pull out each block elements type, so we can read it's state

    info_by_block_id = {}
    for block in blocks:
        block_id = block["block_id"]

        label = block["label"]["text"]
        action_id = block["element"]["action_id"]

        info_by_block_id[block_id] = {
            "label": label,
            "action_id": action_id
        }

    print(info_by_block_id)

    form_values = {}
    for block_id in state:
        label = info_by_block_id[block_id]["label"]
        action_id = info_by_block_id[block_id]["action_id"]

        state_access_path = ""
        if action_id == "static_select-action":
            state_access_path = state[block_id][action_id]["selected_option"]["value"]
        else:
            state_access_path = state[block_id][action_id]["value"]

        form_values[block_id + "_" + label] = state_access_path

    slack_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    bearer_token = "Bearer " + slack_oauth_token

    # Define the URL and headers
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    print(form_values)

    payload = {
        "channel": "C074P84H15Y",
        "text": "Hello world :tada: " + list(form_values.values())[0]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.json())

    return form_values
