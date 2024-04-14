FROM python:3.10

RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY app.py app.py
COPY worker.py worker.py

RUN pip install --upgrade pip
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["/usr/bin/supervisord"]
