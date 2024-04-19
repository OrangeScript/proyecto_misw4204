from ftplib import FTP
from config.global_constants import (
    FTP_ADMIN_USER,
    FTP_PASSWORD,
    FTP_REMOTE_SERVER,
    FTP_VIDEOS_FOLDER,
)


def upload_file_ftp(file, remote_name):
    with FTP(FTP_REMOTE_SERVER) as ftp:
        ftp.login(FTP_ADMIN_USER, FTP_PASSWORD)
        if FTP_VIDEOS_FOLDER not in ftp.nlst():
            ftp.mkd(FTP_VIDEOS_FOLDER)
        ftp.cwd(FTP_VIDEOS_FOLDER)

        ftp.storbinary(f"STOR {remote_name}", file.stream)

        print(
            f"File {remote_name} uploaded successfully to {FTP_VIDEOS_FOLDER}/{remote_name}"
        )
