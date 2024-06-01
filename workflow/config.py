class Config:
    def __init__(self, outcome_type, outcomes):
        self.outcome_type = outcome_type
        self.outcomes = outcomes


workflows = [
    {
        "id": "connected-accounts",
        "steps": [
            {
                "step_id": 1,
                "action": "button_selection",
                "message": "Step 1: What's the issue?",
                "branch": [
                    {
                        "text": "Consent approval screen",
                        "action_id": "connected-accounts_button-click-1",
                        "next_step": 2
                    },
                    {
                        "text": "Easy Transfer",
                        "action_id": "connected-accounts_button-click-2",
                        "next_step": 3
                    }
                ]
            },
            {
                "step_id": 2,
                "action": "button_selection",
                "message": "Step 2: Choose consent approval option",
                "branch": [
                    {
                        "text": "Button 1",
                        "action_id": "connected-accounts_button-click-3",
                        "next_step": 4
                    },
                    {
                        "text": "Button 2",
                        "action_id": "connected-accounts_button-click-4",
                        "next_step": 5
                    },
                    {
                        "text": "Button 3",
                        "action_id": "connected-accounts_button-click-5",
                        "next_step": 6
                    }
                ]
            },
            {
                "step_id": 3,
                "action": "send_message",
                "message": "Step 3: Workflow finished",
            },
            {
                "step_id": 4,
                "action": "open_modal",
            },
        ]
    }
]


def get_next_step_by_action_id(workflow, action_id):
    next_step = 0

    for step in workflow['steps']:
        if "branch" in step:
            for branch in step['branch']:
                if branch['action_id'] == action_id:
                    next_step = branch["next_step"]
                    break
            if next_step != 0:
                break

    for step in workflow['steps']:
        if step['step_id'] == next_step:
            return step


def get_config(next_step):
    reply_type = next_step['action']

    outcomes = []
    if reply_type == 'button_selection':
        for branch in next_step["branch"]:
            outcomes.append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": branch["text"],
                },
                "value": "button_tap_connected_accounts",
                "action_id": branch["action_id"],
            })

    if reply_type == 'send_message':
        outcomes.append(next_step["message"])

    if reply_type == 'open_modal':
        return Config(reply_type, outcomes)

    return Config(reply_type, outcomes)


def get_options(branches):
    elements = []
    for branch in branches:
        elements.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": branch["text"],
            },
            "value": branch["action_id"],
            "action_id": branch["action_id"]
        })

    return elements


def get_workflow(workflow_id):
    for workflow in workflows:
        if workflow["id"] == workflow_id:
            return workflow
