# Demo chatbot for giosg platform

This is a simple example chatbot that works on the [giosg.com](https://www.giosg.com) platform.
It works with giosg's webhook notifications and HTTP APIs, and runs as a [Flask server](http://flask.pocoo.org/).

Please **read the following documentation** so that you understand the basic principles of how chatbots work on giosg platform as "apps":

- [giosg APPS documentation](http://developers.giosg.com/giosg_apps.html)
- [giosg chatbot guide](http://developers.giosg.com/guides.html#chat-bot-guide)

## How it works?

The chatbot has the following functionality:

- When a new chat is routed to the bot, it **automatically joins it and sends a message containing link buttons for different topics**
- Whenever a link topic button is clicked, it sends another message (and offers the same buttons)
- It also offers a **button for inviting a human to the chat**. If clicked, the bot will invite an online team to the chat if found.
- When inviting people, the bot tries to find a team by default with the name "Customer service". This may be configured.
- Finally, after inviting a team, the bot **asks if their help was useful or not**. It then leaves the chat.

## Project structure

- [`requirements.txt`](./requirements.txt) contains Python (PIP) requirements for running and developing the bot
- [`server/conf.py`](./server/conf.py) reads the configuration for the chatbot from the environment variables
- [`server/server.py`](./server/server.py) defines the [Flask server app](http://flask.pocoo.org/) and the URL routings
- [`server/views.py`](./server/views.py) defines the views for handling incoming HTTP requests
- [`server/bot.py`](./server/bot.py) defines the functional logic of the chatbot
- [`server/giosg.py`](./server/giosg.py) defines simple utility functions for making HTTP requests to the [giosg HTTP API](http://developers.giosg.com/http_api.html)
- [`server/tests/`](./server/tests/) contains [unit tests](#running-tests) for the app
- [`server/templates/`](./server/templates/) contains the HTML template for the "front page" of the bot server

## Setting up local dev environment

### Clone the repository

    git clone https://github.com/giosg/demo-bot.git

### Install requirements

Create a **Python 2.7** virtualenv for the project:

    cd demo-bot
    mkvirtualenv -a . -r requirements.txt demo-bot

To later switch to the virtualenv and to the folder:

    workon demo-bot

To ensure that you have the latest PIP requirements installed:

    pip install -r requirements.txt

### Set up environment variables

Add the correct information to your environment variables required by the bot.

**TIP:** You can add these lines to the virtualenv postactive hook file (`$VIRTUAL_ENV/bin/postactivate`), so that they are automatically applied whenever you `workon` on your virtualenv!

``` bash
# REQUIRED: A shared secret that the chatbot requires to be provided as the `secret` parameter in webhook requests
export SECRET_STRING="bEsTsEcReT"
# OPTIONAL: Name of the team which bot will invite to the chats, if online. Defaults to "Customer service"
export INVITEE_TEAM_NAME="Chat agents"
```

### Set up the app

Please follow the [giosg APPs documentation](http://developers.giosg.com/giosg_apps.html) to perform the following steps:

- Create a giosg APP to your organization account, with the webhooks as described below
- Install the app, probably to your own organization, at least while developing
- Route chats from the desired room to the chatbot by adding the created bot user to a router

The chatbot will react to the events in the giosg system.
It needs to be notified by **HTTP webhooks** whenever there are new chats or chat messages.
For this purpose, you need to configure the following webhooks, [as described in the documentation](http://developers.giosg.com/giosg_apps.html#webhooks)

Endpoint URL                                                  | Channel pattern                            | What to subscribe
--------------------------------------------------------------|--------------------------------------------|--------------------------
`https://your-chatbot-host.com/chats?secret=<YOUR_SECRET>`    | `/api/v5/users/{user_id}/routed_chats`     | additions only
`https://your-chatbot-host.com/messages?secret=<YOUR_SECRET>` | `/api/v5/users/{user_id}/chats/*/messages` | additions only

The `<YOUR_SECRET>` needs to be replaced with your custom random secret string you used in `SECRET_STRING` environment variable.
The `your-chatbot-host.com` needs to be replaced with the domain where your chatbot is hosted.

**For local development** using `localhost` won't of course work, as giosg servers cannot reach your local environment.
Instead, you can use a tunneling service, such as [ngrok](https://ngrok.com/). After [launching your local server](#running-dev-environment), tunnel your traffic with this command:

```bash
./ngrok http 5000
```

Then use the printed hostname as `https://your-chatbot-host.com` in the webhook configurations, e.g. `https://a6ea052f.ngrok.io`.

## Running tests

After installing the dependencies, you can run the tests locally:

```bash
python -m unittest discover
```

## Running dev environment

### Native

The Flask application runs locally in `localhost:5000`.
Run the server with the following command.
Use the host `0.0.0.0` if you are using a tunnel such as [ngrok](https://ngrok.com/).

```bash
export FLASK_APP="server/server.py"
flask run --host=0.0.0.0
```

### Docker

You may want to the your docker image locally before publishing it:

1. You must first build image first
  -  `docker build -t <tag_name> .`,
  -  where you show give some human readable tag name that you recognize

2. Run the flask server
  - `docker run -e FLASK_APP=server/server.py -p 5000:8000 <tag_name> flask run --host='0.0.0.0'`
  - Also you have to provide Bot's ID etc as environment variables
