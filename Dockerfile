FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /chess

COPY requirements.txt requirements.txt
run pip3 install -r requirements.txt
