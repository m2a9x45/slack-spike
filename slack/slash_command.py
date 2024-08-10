from dao import commands, workflow
from slack.api import *
from workflow import config

flag_id = "use_v2_slash_command_handler"


def handle_slash_command(data):
    if True:
        handle_slash_command_v2(data=data)
        return

    print(data)

    data_text = data["text"]
    print(data_text)

    esc_path = commands.get_by_id(command=data_text)
    print(esc_path)

    workflow = config.get_workflow(esc_path[0]["workflow_id"])
    first_step = config.get_step_by_id(workflow=workflow, step_id=1)
    workflow_config = config.get_config(first_step)

    slack_fallback_message(
        channel="C074P84H15Y", thread_ts=None, elements=workflow_config.outcomes)


def handle_slash_command_v2(data):
    data_text = data["text"]
    print(data_text)

    esc_path = commands.get_by_id(command=data_text)
    print(esc_path)
    if len(esc_path) == 0:
        print("No command found for:", data_text)
        return

    workflow_id = esc_path[0]["workflow_id"]
    first_step = workflow.get_step_by_id(
        wf_id=workflow_id, step_id=workflow_id+"_step_1")

    if first_step[0]["action"] != "button_selection":
        print("unsupported step action type")
        return

    branches = workflow.get_branches_by_step_id(first_step[0]["step_id"])
    outcomes = []
    for branch in branches:
        print(branch["text"], branch["action_id"])
        outcomes.append({
            "type": "button",
            "text": {
                    "type": "plain_text",
                    "text": branch["text"],
            },
            "value": "button_tap_connected_accounts",
            "action_id": branch["action_id"],
        })

    print(outcomes)

    slack_fallback_message(
        channel="C074P84H15Y", thread_ts=None, elements=outcomes, text=first_step[0]["message"])
