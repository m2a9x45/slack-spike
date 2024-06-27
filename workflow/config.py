class Config:
    def __init__(self, outcome_type, outcomes):
        self.outcome_type = outcome_type
        self.outcomes = outcomes


workflows = [
    {
        "id": "connected-accounts",
        "trigger_id": "open_banking_escalations_C074P84H15Y",
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
                        "next_step": 3
                    },
                    {
                        "text": "Button 3",
                        "action_id": "connected-accounts_button-click-5",
                        "next_step": 3
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
                "branch": [
                    {
                        "next_step": 3
                    },
                ]
            },
        ]
    },
    {
        "id": "easy-transfers",
        "trigger_id": "test_workflow_C074P84H15Y",
        "steps": [
            {
                "step_id": 1,
                "action": "button_selection",
                "message": "Step 1: Hello world",
                "branch": [
                    {
                        "text": "yes",
                        "action_id": "easy-transfers_button-click-1",
                        "next_step": 2
                    },
                    {
                        "text": "no",
                        "action_id": "easy-transfers_button-click-2",
                        "next_step": 3
                    }
                ]
            },
            {
                "step_id": 2,
                "action": "send_message",
                "message": "Step 2: yes",
            },
            {
                "step_id": 3,
                "action": "send_message",
                "message": "Step 3: no",
            }
        ]
    },
    {
        "id": "test-1",
        "trigger_id": "testing_thing_C074P84H15Y",
        "steps": [
            {
                "step_id": 1,
                "action": "button_selection",
                "message": "Select a provider",
                "branch": [
                    {
                        "text": "yes",
                        "action_id": "test-1_button-click-1",
                        "next_step": 2
                    }
                ]
            },
            {
                "step_id": 2,
                "action": "open_modal",
                "input": [
                    {
                        "options": [
                            {"name": "HSBC", "value": "hsbc"},
                            {"name": "Lloyds", "value": "lloyds"},
                            {"name": "TSB", "value": "tsb"},
                        ]
                    }
                ],
                "message": "test",
                "branch": [
                    {
                        "next_step": 4
                    },
                ]
            },
            {
                "step_id": 4,
                "action": "send_message",
                "message": "Step 4: Workflow finished",
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


def get_step_by_id(workflow, step_id):
    for step in workflow['steps']:
        if step["step_id"] == step_id:
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
        if "input" not in next_step:
            return Config(reply_type, [{
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Thing",
                }
            }])

        options = []
        for option in next_step["input"][0]["options"]:
            options.append({
                "text": {
                    "type": "plain_text",
                    "text": option["name"],
                },
                "value": option["value"]
            })

        outcomes.append({
            "type": "input",
            "element": {
                    "type": "static_select",
                    "placeholder": {
                            "type": "plain_text",
                        "text": "Select an item",
                    },
                "options": options,
                "action_id": "static_select-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Label",
            }
        })

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


def get_workflow_by_trigger_id(trigger_id):
    print(trigger_id)
    for workflow in workflows:
        if workflow["trigger_id"] == trigger_id:
            return workflow
