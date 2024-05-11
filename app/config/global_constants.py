import os
import sys

from dotenv import load_dotenv

DEV_ARG_VALUE = "dev"

if len(sys.argv) > 1 and sys.argv[1] == DEV_ARG_VALUE:
    print("\n* Running on develop mode\n")
    try:
        load_dotenv("dev.env")
    except FileNotFoundError:
        pass

else:
    print("\n* Running on production mode\n")
    try:
        load_dotenv("prod.env")
    except FileNotFoundError:
        pass

# DB
SQL_DOMAIN = os.getenv("SQL_DOMAIN")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")
SQL_DB = os.getenv("SQL_DB")

# LOCAL FILES CONFIGURATION
LOGO_VIDEO_ITEM_NAME = os.getenv("LOGO_VIDEO_ITEM_NAME")
LOGO_NAME = os.getenv("LOGO_NAME")
VIDEO_FOLDER_NAME = os.getenv("VIDEO_FOLDER_NAME")
ASSETS_PATH = os.getenv("ASSETS_PATH")
LOGO_FOLDER_NAME = os.getenv("LOGO_FOLDER_NAME")
OUTPUT_VIDEO_NAME = os.getenv("OUTPUT_VIDEO_NAME")
GLOBAL_VIDEO_SIZE = os.getenv("GLOBAL_VIDEO_SIZE")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
VALID_VIDEO_EXTENSIONS = [".mp4"]

# GOOGLE CLOUD STORAGE
GOOGLE_CLOUD_STORAGE_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
GOOGLE_CLOUD_STORAGE_CREDENTIALS = os.getenv("GOOGLE_CLOUD_STORAGE_CREDENTIALS")

# GOOGLE CLOUD PUB/SUB
GOOGLE_CLOUD_PUB_SUB_TOPIC_PATH = os.getenv("GOOGLE_CLOUD_PUB_SUB_TOPIC_PATH")
GOOGLE_CLOUD_PUB_SUB_TOPIC_ERROR_PATH = os.getenv(
    "GOOGLE_CLOUD_PUB_SUB_TOPIC_ERROR_PATH"
)
GOOGLE_CLOUD_PUB_SUB_SUBSCRIPTION_PATH = os.getenv(
    "GOOGLE_CLOUD_PUB_SUB_SUBSCRIPTION_PATH"
)
GOOGLE_CLOUD_PUB_SUB_SUBSCRIPTION_ERROR_PATH = os.getenv(
    "GOOGLE_CLOUD_PUB_SUB_SUBSCRIPTION_ERROR_PATH"
)
GOOGLE_CLOUD_PUB_SUB_CREDENTIALS = os.getenv("GOOGLE_CLOUD_PUB_SUB_CREDENTIALS")

# API
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
JWT_EXPIRATION_TIME = int(os.getenv("JWT_EXPIRATION_TIME"))
MAX_CONTENT_LENGTH = 25 * 1024 * 1024

# SYSTEM
IS_IN_DEVELOP = len(sys.argv) > 1 and sys.argv[1] == DEV_ARG_VALUE
