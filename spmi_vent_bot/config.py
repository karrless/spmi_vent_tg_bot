import os
from dotenv import load_dotenv


load_dotenv()

def get_env(name: str):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"В .env нет значения {name}")


DEBUG = get_env("DEBUG")

TOKEN = get_env("TOKEN")

DB_URI = get_env("DB_URI")