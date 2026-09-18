import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_HOST = os.getenv("DB_HOST")

    SECRET_KEY = os.getenv("SECRET_KEY")
    HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
    TOKEN_EXPIRY = os.getenv("TOKEN_EXPIRY")

    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
