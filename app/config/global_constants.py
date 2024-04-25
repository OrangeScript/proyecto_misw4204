import os
import sys

from dotenv import load_dotenv

if len(sys.argv) > 1 and sys.argv[1] == "dev":
    print("\n* Running on develop mode\n")
    try:
        load_dotenv("dev.env")
    except FileNotFoundError:
        pass

if len(sys.argv) > 1 and sys.argv[1] == "test":
    print("\n* Running on test mode\n")
    try:
        load_dotenv("test.env")
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

# RABBIT
RABBITMQ_SERVER_HOST = os.getenv("RABBITMQ_SERVER_HOST")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")
RABBIT_ADMIN_USER = os.getenv("RABBIT_ADMIN_USER")
RABBIT_ADMIN_PASSWORD = os.getenv("RABBIT_ADMIN_PASSWORD")

# LOCAL FILES
LOGO_VIDEO_ITEM_NAME = os.getenv("LOGO_VIDEO_ITEM_NAME")
LOGO_NAME = os.getenv("LOGO_NAME")
VIDEO_FOLDER_NAME = os.getenv("VIDEO_FOLDER_NAME")
ASSETS_PATH = os.getenv("ASSETS_PATH")
LOGO_FOLDER_NAME = os.getenv("LOGO_FOLDER_NAME")
OUTPUT_VIDEO_NAME = os.getenv("OUTPUT_VIDEO_NAME")
GLOBAL_VIDEO_SIZE = os.getenv("GLOBAL_VIDEO_SIZE")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# FTP SERVER
FTP_REMOTE_SERVER = os.getenv("FTP_REMOTE_SERVER")
FTP_DEPLOY_SERVER = os.getenv("FTP_DEPLOY_SERVER")
FTP_ADMIN_USER = os.getenv("FTP_ADMIN_USER")
FTP_PASSWORD = os.getenv("FTP_PASSWORD")
FTP_VIDEOS_FOLDER = os.getenv("FTP_VIDEOS_FOLDER")
VALID_VIDEO_EXTENSIONS = [".mp4"]

# API
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")

# SYSTEM
IS_IN_DEVELOP = len(sys.argv) > 1 and (sys.argv[1] == "dev" or sys.argv[1] == "test")
