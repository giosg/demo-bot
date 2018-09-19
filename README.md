# Hogwarts Bot & Rich Chat Message Demo

This is a demo provided by Hogwarts to show what you can achieve with bots and rich chat messages. This is done via using Giosg's HTTP APIs with Flask server.

## Setting up local dev environment

### Clone the repository

    git clone git@github.com:giosg/demo-bot.git

### Install requirements

Create a **Python 2.7** virtualenv for the project:

    cd demo-bot
    mkvirtualenv -a . -r requirements.txt demo-bot

To later switch to the virtualenv and to the folder:

    workon demo-bot

To ensure that you have the latest PIP requirements installed:

    pip install -r requirements.txt

### Install a giosg app

Check the guide for setting up a *giosg APP* for the Chat Bot.
You need to define a webhook for the following channel:

    /api/v5/orgs/{organization_id}/owned_chats/*/messages

Any *additions* to this channel should be notified to the following URL:

    http://localhost:5000/chat_messages?secret=bEsTsEcReT

The `secret` should be replaced with your custom random secret string.

### Set up environment variables

Add the correct information to your environment variables required by the bot.

**TIP:** You can add these lines to the virtualenv postactive hook file (`$VIRTUAL_ENV/bin/postactivate`), so that they are automatically applied whenever you `workon` on your virtualenv!

``` bash
# REQUIRED: A shared secret that the chatbot requires to be provided as the `secret` parameter in webhook requests
export SECRET_STRING="bEsTsEcReT"
# OPTIONAL: Name of the team which bot will invite (if online). Defaults to "Customer service"
export INVITEE_TEAM_NAME="Chat agents"
```

## Running dev environment

### Native

Our Flask application runs locally in `localhost:5000`

Run the server

```bash
export FLASK_APP="server/server.py"
flask run
```

### Docker

You may want to the your docker image locally before publishing it:

1. You must first build image first
  -  `docker build -t <tag_name> .`,
  -  where you show give some human readable tag name that you recognize

2. Run the flask server
  - `docker run -e FLASK_APP=server/server.py -p 5000:8000 <tag_name> flask run --host='0.0.0.0'`
  - Also you have to provide Bot's ID etc as environment variables
