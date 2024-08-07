from flask import request
from dao import workflow


def read_workflow():
    wf_steps = workflow.list_all_wf_steps_by_id("wf-test")

    for step in wf_steps:
        branches = workflow.get_branches_by_step_id(step_id=step["step_id"])
        step["branches"] = branches

    return wf_steps, 200
