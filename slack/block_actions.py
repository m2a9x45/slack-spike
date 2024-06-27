from slack.api import *
from workflow import config, store


# TODO: Update the message that the block action is coming from to disable the button, using the `chat.update` API?
def block_actions(data):
    if "actions" not in data:
        return

    action_id = data["actions"][0]["action_id"]
    thread_ts = data["container"]["thread_ts"]
    channel = data["container"]["channel_id"]

    # Get the workflowID from the actionID
    workflow_id = action_id.split("_")[0]
    workflow = config.get_workflow(workflow_id)

    next_step = config.get_next_step_by_action_id(workflow, action_id)

    workflow_config = config.get_config(next_step)
    if workflow_config is None:
        return

    match workflow_config.outcome_type:
        case "send_message":
            slack_send_message(
                channel=channel, thread_ts=thread_ts, text=workflow_config.outcomes[0])
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
