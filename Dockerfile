# syntax=docker/dockerfile:1

# FROM python:3.9-alpine
FROM python:3.9-slim-buster

RUN apt-get -y update
RUN apt-get -y install libsodium23
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install flask==1.1.4 threema.gateway==5.0.0 fritzconnection
# RUN pip3 install flask==2.0.2 threema.gateway==5.0.0 fritzconnection
# RUN pip3 install -r requirements.txt

COPY app.py .
COPY monitor/ monitor/
COPY monitor.ini .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
