import os
from dotenv import load_dotenv
from spmi_vent_bot.errors import MissingEnvironmentVariable

load_dotenv()

def get_env(name: str):
    try:
        return os.environ[name]
    except KeyError:
        raise MissingEnvironmentVariable(name)


DEBUG = get_env("DEBUG")

TOKEN = get_env("TOKEN")

DB_URI = get_env("DB_URI")