from functools import wraps
import json

from flask import Flask, request, g
from flask_cors import CORS
from dotenv import load_dotenv

from slack.view_submission import view_submission
from slack.shortcut import shortcut
from slack.events import handle_event
from slack.block_actions import block_actions
from slack.slash_command import handle_slash_command

from routes.commands import *
from routes.oauth_slack import *
from routes.workflow import *

load_dotenv()

app = Flask(__name__)
cors = CORS(app, supports_credentials=True,
            resources={r"/*": {"origins": ["https://7d7b-31-53-104-139.ngrok-free.app", "http://localhost:5173"]}})


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        if not user_id:
            return {"error": "User not authenticated"}, 403
        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/wf/<wf_id>', methods=['GET'])
def workflow(wf_id):
    return read_workflow(wf_id)


@app.route('/wf/step/update', methods=['POST'])
def updateWorkflowStep():
    return update_workflow_step(request.json)


@app.route('/wf/step/create', methods=['POST'])
def createWorkflowStep():
    return create_workflow_step(request.json)


@app.route('/wf/step/branch/create', methods=['POST'])
def createWorkflowBranch():
    return create_workflow_branch(request.json)


@app.route('/wf/step/location/<wf_id>', methods=['GET'])
def readWorkflowStepLocation(wf_id):
    return read_workflow_step_location(wf_id)


@app.route('/wf/step/location', methods=['POST'])
def saveWorkflowStepLocation():
    return save_workflow_step_location(request.json)


@app.route('/oauth/slack', methods=['POST'])
def slack_oauth():
    return handle_oauth_slack()


@app.route('/whoami')
def whoami():
    user = request.cookies.get('user_id')
    # print(user)
    return {"message": "success", "user": user}, 200


@app.route('/slash', methods=['GET'])
@login_required
def slash_list():
    print(g.user_id)
    return list_commands()


@app.route('/slash', methods=['POST'])
def slash():
    return set_command()


@app.route('/events', methods=['POST'])
def events():
    data = request.json
    return handle_event(data)


# https://api.slack.com/interactivity/slash-commands
@app.route('/slack-command', methods=['POST'])
def command():
    data = request.form
    handle_slash_command(data)
    return "", 200


# Guide on what payload shortcut payload look like:
# https://api.slack.com/reference/interaction-payloads/shortcuts
@app.route('/slack', methods=['POST'])
def handle_slack():
    # print("Form Data:", request.form["payload"])
    # Parse the payload as JSON
    data = json.loads(request.form["payload"])
    # Print the parsed JSON data
    # print("Parsed Data:", data)

    match data['type']:
        case 'view_submission':
            view_submission(data)
            return "", 200
        case 'shortcut':
            shortcut(data)
            return "", 200
        case "block_actions":
            block_actions(data)
            return "", 200

    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
