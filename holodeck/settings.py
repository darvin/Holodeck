
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)


style = "vinkpunk"
