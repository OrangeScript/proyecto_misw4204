# proyecto_misw4204 - International FPV Drone Racing League

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/postgreSQL-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Configuración del entorno

### PostgreSQL

Asegúrate de tener PostgreSQL instalado y configurado en tu sistema. Puedes descargarlo desde [el sitio oficial de PostgreSQL](https://www.postgresql.org/download/).

### Docker (opcional)

Puedes descargar Docker desde [el sitio oficial de Docker](https://www.docker.com/get-started).

### Instalación de FFmpeg

FFmpeg es una herramienta de línea de comandos para grabar, convertir y reproducir audio y video. Es una herramienta poderosa y versátil para trabajar con multimedia en sistemas operativos Linux, Windows y macOS.

- **Linux:**
  ```bash
  sudo apt-get install ffmpeg
  ```
- **macOs:**
  ```bash
  brew install ffmpeg
  ```
- **Windows:**
  1.  Descarga un archivo zip de FFmpeg desde el [sitio oficial de FFmpeg](https://ffmpeg.org/download.html).
  2.  Extrae el contenido del archivo zip en una carpeta de tu elección.
  3.  Agrega la ruta de la carpeta de FFmpeg al PATH del sistema para poder ejecutar FFmpeg desde cualquier ubicación en la línea de comandos.

## Ejecutar la aplicación

### Modo desarrollo

Para ejecutar la aplicación en modo desarrollo, sigue estos pasos:

1. En una terminal, navega hasta la carpeta `app` del proyecto.
2. Ejecuta el siguiente comando para iniciar la API Flask en modo desarrollo:

   ```bash
   python app.py dev
   ```

3. En otra terminal, navega hasta la carpeta `app` del proyecto.
4. Ejecuta el siguiente comando para iniciar el worker en modo desarrollo:

   ```bash
   python worker.py dev
   ```

### Modo producción

Para ejecutar la aplicación en modo producción, sigue estos pasos:

1. En una terminal, navega hasta la carpeta `app` del proyecto.
2. Ejecuta el siguiente comando para iniciar la API Flask en modo producción:

   ```bash
   python app.py
   ```

3. En otra terminal, navega hasta la carpeta `app` del proyecto.
4. Ejecuta el siguiente comando para iniciar el worker en modo producción:

   ```bash
   python worker.py
   ```

## Levantar el entorno completo con docker

En la carpeta raiz se encuentra un de Docker compose, el cual se llama **docker-compose.yaml**, para levantar la aplicación solo es necesario ejecutar el siguiente comando:

```bash
docker-compose up
```
