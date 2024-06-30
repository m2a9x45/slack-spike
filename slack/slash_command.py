from dao import commands
from slack.api import *
from workflow import config


def handle_slash_command(data):
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
