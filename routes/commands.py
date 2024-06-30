from flask import request
from dao import commands


def set_command():
    data = request.json

    commands.create(
        path_id=data["path_id"], command=data["command"], worflow_id=data["workflow_id"])

    return {"message": "success"}, 200


def list_commands():
    return commands.get_all()
