"""
Collect the app settings from the environment variables as Python constants.
"""
import os

INVITEE_TEAM_ID = os.environ["INVITEE_TEAM_ID"]
SERVICE_URL = os.environ.get("SERVICE_URL") or 'https://service.giosg.com'
SECRET_STRING = os.environ["SECRET_STRING"]
