from slack.api import slack_api
from workflow.config import get_config


# TODO: Update the message that the block action is coming from to disable the button
# Can maybe use the `chat.update` API?
def block_actions(data):
    if "actions" not in data:
        return

    action_id = data["actions"][0]["action_id"]
    thread_ts = data["container"]["thread_ts"]
    channel = data["container"]["channel_id"]

    config = get_config(action_id=action_id)
    if config is None:
        return

    match config.outcome_type:
        case "text":
            slack_api('https://slack.com/api/chat.postMessage', {
                "channel": channel,
                "thread_ts": thread_ts,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": config.outcomes[0]
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
                        "elements": config.outcomes
                    }
                ]
            })
