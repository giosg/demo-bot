"""
Collect the app settings from the environment variables as Python constants.
"""
import os

INVITEE_TEAM_NAMES = {
    'en': os.environ.get('INVITEE_TEAM_NAME_EN') or 'Customer service',
    'fi': os.environ.get('INVITEE_TEAM_NAME_FI') or 'Customer service (FI)',
}
SERVICE_URL = os.environ.get("SERVICE_URL") or 'https://service.giosg.com'
SECRET_STRING = os.environ["SECRET_STRING"]
