class Config:
    def __init__(self, outcome_type, outcomes):
        self.outcome_type = outcome_type
        self.outcomes = outcomes


def get_config(action_id):
    actions = {
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

    if action_id not in actions:
        print("Unsupported action_id:", action_id)
        return

    reply_type = ""
    for key, value in actions[action_id].items():
        if key == "type":
            reply_type = value

    outcomes = []
    for key, value in actions[action_id].items():
        match reply_type:
            case "text":
                outcomes.append(actions[action_id]["text"])
            case "modal":
                break
            case _:
                outcomes.append({
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": value,
                    },
                    "value": "button_tap_connected_accounts",
                    "action_id": key
                })

    return Config(reply_type, outcomes)


def get_options():
    # TODO: Based on the channelID / message, we want to return the correct workflow
    options = [
        {
            "text": "Consent approval screen not showing account",
            "action_id": "button_click_unique_1"
        },
        {
            "text": "Something something easy transfer",
            "action_id": "button_click_unique_2"
        },
        {
            "text": "Connected mortgages",
            "action_id": "button_click_unique_3"
        },
        {
            "text": "Something else thing",
            "action_id": "button_click_unique_4"
        }
    ]

    elements = []
    for option in options:
        elements.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": option["text"],
            },
            "value": option["action_id"],
            "action_id": option["action_id"]
        })

    return elements