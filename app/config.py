import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = "SmartDoc AI"
APP_VERSION = "0.1.0"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")