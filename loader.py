import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()
TOKEN_BOT = os.getenv("BOT_TOKEN")
HOST = os.getenv("DB_HOST")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_DATABASE")
PORT = os.getenv("DB_PORT")
KEITARO_IP = os.getenv("KEITARO_IP")
ADMIN = os.getenv("BOT_ADMINS")
SUPPORT = os.getenv("BOT_SUPPORT")
KEIARO_ADMIN_TOKEN = os.getenv("KEIARO_ADMIN_TOKEN")

if "," in ADMIN:
    ADMIN = ADMIN.split(",")
else:
    if len(ADMIN) >= 1:
        ADMIN = [ADMIN]
    else:
        print("Admin ID is not specified")

storage = MemoryStorage()
bot = Bot(TOKEN_BOT, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)