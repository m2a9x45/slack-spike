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

    return form_values
