import os
from dotenv import load_dotenv
from spmi_vent_bot.errors import MissingEnvironmentVariable

load_dotenv()

DEBUG = os.getenv("DEBUG")
TOKEN = os.getenv("TOKEN")

if any(list(map(lambda x: x is None,[DEBUG, TOKEN]))):
    raise MissingEnvironmentVariable