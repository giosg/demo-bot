# Hogwarts Bot & Rich Chat Message Demo

This is a demo provided by Hogwarts to show what you can achieve with bots and rich chat messages. This is done via using Giosg's HTTP APIs with Flask server.

## Setting up local dev environment

### Install requirements

You should have your own virtualenv for this.
`pip install -r requirements.txt`

### Install Bot user for this

Check the guide for setting up Chat Bot. Then fill the correct information to `dev.py`

## Running dev environment

Our Flask application runs locally in `localhost:5000`

### Native

1. Export the Flask Application to enviroment variables
  - `export FLASK_APP=server/server.py`
2. Run the server
  - `flask run`

### Docker

You may want to the your docker image locally before publishing it:

1. You must first build image first
  -  `docker build -t <tag_name> .`,
  -  where you show give some human readable tag name that you recognize

2. Run the flask server
  - `docker run -e FLASK_APP=server/server.py -p 5000:8000 <tag_name> flask run --host='0.0.0.0'`

### Publishing a new Docker image

You must have login credentials to Giosg docker hub. After this you can start publishing.

1. `docker login`
2. `docker push giosg/hogwarts_bot_demo:<tag_name>`

Cheers! Your docker image is now uploaded to Giosg's docker hub and you may start using it.
