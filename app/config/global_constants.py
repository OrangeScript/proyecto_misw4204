import os
from dotenv import load_dotenv

try:
    load_dotenv("conf.env")
except FileNotFoundError:
    pass

SQL_DOMAIN = os.getenv("SQL_DOMAIN")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")
SQL_DB = os.getenv("SQL_DB")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")
GLOBAL_VIDEO_SIZE = os.getenv("GLOBAL_VIDEO_SIZE")

LOGO_VIDEO_ITEM_NAME = os.getenv("LOGO_VIDEO_ITEM_NAME")
LOGO_NAME = os.getenv("LOGO_NAME")
VIDEO_FOLDER_NAME = os.getenv("VIDEO_FOLDER_NAME")
ASSETS_PATH = os.getenv("ASSETS_PATH")
LOGO_FOLDER_NAME = os.getenv("LOGO_FOLDER_NAME")
OUTPUT_VIDEO_NAME = os.getenv("OUTPUT_VIDEO_NAME")

FTP_REMOTE_SERVER = os.getenv("FTP_REMOTE_SERVER")
FTP_DEPLOY_SERVER = os.getenv("FTP_DEPLOY_SERVER")
FTP_ADMIN_USER = os.getenv("FTP_ADMIN_USER")
FTP_PASSWORD = os.getenv("FTP_PASSWORD")
FTP_VIDEOS_FOLDER = os.getenv("FTP_VIDEOS_FOLDER")
