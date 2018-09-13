"""
Collect the app settings from the environment variables as Python constants.
"""
import os

BOT_USER_ID = os.environ["BOT_USER_ID"]
BOT_USER_API_TOKEN = os.environ["BOT_USER_API_TOKEN"]
BOT_USER_ORGANIZATION_ID = os.environ["BOT_USER_ORGANIZATION_ID"]
ALLOWED_ROOM_ID = os.environ["ALLOWED_ROOM_ID"]
INVITEE_TEAM_ID = os.environ["INVITEE_TEAM_ID"]
# Url where the service is located e.g. http://localhost:8000
SERVICE_URL = os.environ["SERVICE_URL"]
SECRET_STRING = os.environ["SECRET_STRING"]
