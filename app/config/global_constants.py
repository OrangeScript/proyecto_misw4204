import os
import sys

from dotenv import load_dotenv

DEV_ARG_VALUE = "dev"

if len(sys.argv) > 1 and sys.argv[1] == DEV_ARG_VALUE:
    print("\n* Running on develop mode\n")
    try:
        load_dotenv("local.env")
    except FileNotFoundError:
        pass

else:
    print("\n* Running on production mode\n")
    try:
        load_dotenv(".env")
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

CREDENTIALS_INFO_PUB_SUB = {
    "type": os.getenv("TYPE_PUB_SUB_CREDENTIALS"),
    "project_id": os.getenv("PROJECT_ID_PUB_SUB_CREDENTIALS"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID_PUB_SUB_CREDENTIALS"),
    "private_key": os.getenv("PRIVATE_KEY_PUB_SUB_CREDENTIALS"),
    "client_email": os.getenv("CLIENT_EMAIL_PUB_SUB_CREDENTIALS"),
    "client_id": os.getenv("CLIENT_ID_PUB_SUB_CREDENTIALS"),
    "auth_uri": os.getenv("AUTH_URI_PUB_SUB_CREDENTIALS"),
    "token_uri": os.getenv("TOKEN_URI_PUB_SUB_CREDENTIALS"),
    "auth_provider_x509_cert_url": os.getenv(
        "AUTH_PROVIDER_X509_CERT_URL_PUB_SUB_CREDENTIALS"
    ),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL_PUB_SUB_CREDENTIALS"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN_PUB_SUB_CREDENTIALS"),
}


CREDENTIALS_INFO_CLOUD_STORAGE = {
    "type": os.getenv("TYPE_CLOUD_STORAGE_CREDENTIALS"),
    "project_id": os.getenv("PROJECT_ID_CLOUD_STORAGE_CREDENTIALS"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID_CLOUD_STORAGE_CREDENTIALS"),
    "private_key": os.getenv("PRIVATE_KEY_CLOUD_STORAGE_CREDENTIALS"),
    "client_email": os.getenv("CLIENT_EMAIL_CLOUD_STORAGE_CREDENTIALS"),
    "client_id": os.getenv("CLIENT_ID_CLOUD_STORAGE_CREDENTIALS"),
    "auth_uri": os.getenv("AUTH_URI_CLOUD_STORAGE_CREDENTIALS"),
    "token_uri": os.getenv("TOKEN_URI_CLOUD_STORAGE_CREDENTIALS"),
    "auth_provider_x509_cert_url": os.getenv(
        "AUTH_PROVIDER_X509_CERT_URL_CLOUD_STORAGE_CREDENTIALS"
    ),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL_CLOUD_STORAGE_CREDENTIALS"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN_CLOUD_STORAGE_CREDENTIALS"),
}
