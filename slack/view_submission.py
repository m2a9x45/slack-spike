import os
import requests
import json


# Handles model submissions, currently only supports the text input felid
# https://api.slack.com/surfaces/modals#interactions
def view_submission(data):
    blocks = data["view"]["blocks"]
    state = data["view"]["state"]["values"]

    label_by_block_id = {}
    for block in blocks:
        block_id = block["block_id"]
        label = block["label"]["text"]
        label_by_block_id[block_id] = label

    form_values = {}
    for block_id in state:
        label = label_by_block_id[block_id]
        form_values[block_id + "_" + label] = state[block_id]["plain_text_input-action"]["value"]

    slack_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    bearer_token = "Bearer " + slack_oauth_token

    # Define the URL and headers
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
    }

    payload = {
        "channel": "C074P84H15Y",
        "text": "Hello world :tada: " + form_values["K73Vi_Thing"]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.json())

    return form_values
