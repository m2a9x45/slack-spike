import json

from flask import Flask, request
from dotenv import load_dotenv

from slack.view_submission import view_submission
from slack.shortcut import shortcut
from slack.events import handle_event
from slack.block_actions import block_actions

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/events', methods=['POST'])
def events():
    data = request.json
    return handle_event(data)


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
