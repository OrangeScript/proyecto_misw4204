import os
from ftplib import FTP
from config.global_constants import (
    FTP_ADMIN_USER,
    FTP_PASSWORD,
    FTP_REMOTE_SERVER,
    FTP_VIDEOS_FOLDER,
)


def get_asset_path(type, name):
    try:
        project_path = "assets/"
        return f"{project_path}{type}/{name}"
    except Exception as e:
        print(f"\nError getting asset path: {e}")
        return None


def upload_file_ftp(file, remote_name):
    with FTP(FTP_REMOTE_SERVER) as ftp:
        ftp.login(FTP_ADMIN_USER, FTP_PASSWORD)

        # Verificar si la carpeta remota existe
        if "/ftp" + "/" + "videos_1" not in ftp.nlst():
            ftp.mkd("/ftp" + "/" + "videos_1")

        # Cambiar al directorio remoto
        ftp.cwd("/ftp" + "/" + "videos_1")

        ftp.storbinary(f"STOR {remote_name}", file.stream)

        print(
            f"File {remote_name} uploaded successfully to {FTP_VIDEOS_FOLDER}/{remote_name}"
        )


def create_directory_ftp(ftp, directory):
    try:
        ftp.mkd(directory)
        print(f"Directorio '{directory}' creado correctamente.")
    except Exception as e:
        print(f"No se pudo crear el directorio '{directory}': {e}")


def create_path_ftp(path):
    # Configura las credenciales y la conexión al servidor FTP
    ftp = FTP(FTP_REMOTE_SERVER)
    ftp.login(user=FTP_ADMIN_USER, passwd=FTP_PASSWORD)

    # Divide la ruta en partes
    parts = path.split("/")
    current_path = ""

    # Crea cada directorio en la ruta si no existe
    for part in parts:
        current_path = f"{current_path}/{part}"
        create_directory_ftp(ftp, current_path)

    # Cierra la conexión FTP
    ftp.quit()
