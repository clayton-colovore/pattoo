"""Initialize the PATTOO_API_AGENT module."""

# Import PIP3 libraries
from flask import Flask

# Define the global URL prefix
from PattooShared.constants import PATTOO_API_AGENT_PREFIX

# Import PATTOO_API_AGENT Blueprints
from pattoo.api.agents.post import POST
from pattoo.api.agents.status import STATUS

# Setup flask
PATTOO_API_AGENT = Flask(__name__)

# Register Blueprints
PATTOO_API_AGENT.register_blueprint(
    POST, url_prefix=PATTOO_API_AGENT_PREFIX)
PATTOO_API_AGENT.register_blueprint(
    STATUS, url_prefix=PATTOO_API_AGENT_PREFIX)
