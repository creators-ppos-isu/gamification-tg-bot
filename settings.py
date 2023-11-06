from pathlib import Path
from dotenv import load_dotenv
from os import getenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_URL = BASE_DIR / 'db.sqlite3'
BOT_TOKEN = getenv("BOT_TOKEN")
ADMINS = (596546865,)