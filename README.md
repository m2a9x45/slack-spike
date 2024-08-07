# Project overview
Prototype to understand how slack models work for collecting form data. 

## Dev setup

### Database
You'll want to connect to a mysql database and then run the migration file & seed files

- `mysql -h 127.0.0.1 -P 4000 -u root -p`
- `source \slack-spike\config\2024-06-30_migration.sql`
- `source \slack-spike\config\seed\commands.sql`

### Backend

Using python virtual environments:
- `python3 -m venv env` (create a virtual environment)
- On Mac & Linus: `source env/bin/activate` (use the virtual environment)
- On Windows: `.\env\Scripts\activate`

Install dependancies form pip:
- `pip install -r requirements.txt`

You'll want to use a slack sandbox environment, which can be setup via https://api.slack.com/developer-program 

Copy the bot's [user OAuth token](https://api.slack.com/apps/A074RSJEQA0/oauth) to the .env 
file `SLACK_BOT_USER_OAUTH_TOKEN`

Start the backend:
```shell
python3 main.py
```

Start ngrok so slack can talk to us 
```shell
ngrok http http://127.0.0.1:5000
```

Ngrok allows starting mutiple tunnels within a single agent session:
```shell
ngrok start --all
```

```yaml
tunnels:
  httpbin:
    proto: http
    addr: 5000
  demo:
    proto: http
    addr: 5173
```

### Slack setup

// TODO: Add steps for setting a oauth redirect url, to support sign-in with Slack

Update the slack bot's interactivity & shortcut's [request url](https://api.slack.com/apps/A074RSJEQA0/interactive-messages) to match the url from 
ngrok

```shell
https://{uuid}.ngrok-free.app/slack
```

Update the slack bot's event subscription's [request url](https://api.slack.com/apps/A074RSJEQA0/event-subscriptions) to match the url from ngrok

```shell
https://{uuid}.ngrok-free.app/events
```

Add a [new slash command](https://api.slack.com/apps/A074RSJEQA0/slash-commands) to the bot; with a command of `/esc` & a request url matching ngrok

```shell
https://{uuid}.ngrok-free.app/slack-command
```

### ProtoType
1. We take the input from a Slack form submission
2. Check if we support solving this problem
3. Apply rules which ask more question or give an answer