# D:\TIMELINEPROJECT\Timeline_flask_project\timeline_flask\config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Take environment variables from .env.

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
