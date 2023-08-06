import os

TEMP_FOLDER = ".servicefoundry_templates"
ENABLE_CLUSTER_COMMANDS = False
ENABLE_AUTHORIZE_COMMANDS = False
ENABLE_SECRETS_COMMANDS = False
IS_DEBUG = True if os.getenv("SFY_DEBUG") else False
MAX_WIDTH = 100
