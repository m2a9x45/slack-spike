from flask import request
from dao import workflow


def read_workflow():
    wf_steps = workflow.list_all_wf_steps_by_id("wf-test")

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
