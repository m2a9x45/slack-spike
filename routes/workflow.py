from flask import request
from dao import workflow

import uuid


def read_workflow(wf_id):
    wf_steps = workflow.list_all_wf_steps_by_id(wf_id)

    for step in wf_steps:
        branches = workflow.get_branches_by_step_id(step_id=step["step_id"])
        step["branches"] = branches

    return wf_steps, 200


def update_workflow_step(new_step):
    print(new_step)

    updated_step = workflow.update_workflow_step(
        new_step["step_id"], new_step["message"])

    for branch in new_step["branches"]:
        updated_branch = workflow.update_branch(
            id=branch["id"], next_step_id=branch["next_step_id"], message=branch["text"])
        print("branch updated:" + str(updated_branch) +
              " " + str(branch["id"]))

    print("step updated" + str(updated_step))

    return "", 200


def create_workflow_step(data):
    print(data)

    step_id = data["wf_id"] + "_step_1"

    wf_steps = read_workflow(data["wf_id"])
    print(len(wf_steps[0]))
    if len(wf_steps[0]) == 0:
        step_id = data["wf_id"] + "_step_1"
    else:
        step_id = data["wf_id"] + "_step_" + str(len(wf_steps[0]) + 1)

    print(step_id)

    workflow.create_step(wf_id=data["wf_id"], step_id=step_id,
                         action=data["action"], message=data["message"])

    return data, 200


def create_workflow_branch(data):
    print(data)

    workflow.create_branch(step_id=data["step_id"], action_id=str(
        uuid.uuid4()), next_step_id=data["next_step_id"], text=data["action"])

    return "", 200


def read_workflow_step_location(step_id):
    print(step_id)
    locations = workflow.read_step_locations(step_id=step_id)
    print("hi", locations)
    return locations, 200


def save_workflow_step_location(data):
    wf_id = data["wf_id"]

    for key in data["locations"]:
        step = data["locations"][key]
        print(key, step["left"], step["top"])

        location_for_step_id = workflow.read_step_locations(step_id=key)
        if len(location_for_step_id) != 0:
            workflow.update_step_location(
                step_id=key, left=step["left"], top=step["top"])
        else:
            workflow.create_step_location(
                wf_id=wf_id, step_id=key, left=step["left"], top=step["top"])

    return "", 200
