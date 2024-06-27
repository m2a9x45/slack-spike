from slack.api import *
from workflow import config, store


# Handles model submissions, currently only supports the text input felid
# https://api.slack.com/surfaces/modals#interactions
def view_submission(data):
    blocks = data["view"]["blocks"]
    state = data["view"]["state"]["values"]

    # We'll want to store form_values at some point
    # This is the data the customer entered into the model who's submission is being handled
    form_values = get_state(blocks=blocks, state=state)
    print(form_values)

    callback_id = data["view"]["callback_id"]
    callback_date = store.get_store(callback_id)

    workflow_id = callback_date["workflow_id"]
    channel = callback_date["channel"]
    thread_ts = callback_date["thread"]
    next_step = callback_date["next_step"]

    workflow = config.get_workflow(workflow_id)
    workflow_next_step = config.get_step_by_id(
        workflow=workflow, step_id=next_step)
    workflow_config = config.get_config(workflow_next_step)

    match workflow_config.outcome_type:
        case "send_message":
            slack_send_message(
                channel=channel, thread_ts=thread_ts, text=workflow_config.outcomes[0] + " " + list(form_values.values())[0])
            return
        case "open_modal":
            # TODO: If any workflow has mutiple model steps, we'll want to update the callback object store with the new data
            model_close_next_step = next_step["branch"][0]["next_step"]

            id = store.add_callback(
                workflow_id=workflow_id, channel=channel, thread_ts=thread_ts, next_step=model_close_next_step)
            trigger_id = data["trigger_id"]
            slack_open_model(trigger_id=trigger_id,
                             blocks=workflow_config.outcomes, callback_id=id)
            return
        case _:
            slack_fallback_message(
                channel=channel, thread_ts=thread_ts, elements=workflow_config.outcomes)
            return


# Will extract the users selected responses from the model
def get_state(blocks, state):
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
    return form_values
