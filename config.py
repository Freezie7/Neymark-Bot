import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")