FROM ubuntu:20.04

RUN  apt-get update -y && apt-get install -y  python3-pip python3-dev build-essential

FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

RUN mkdir /nutrition

WORKDIR /nutrition

COPY . /nutrition

SHELL ["/bin/bash", "-c"]

RUN python3 -m venv nutrition/venv && pip install -r requirements.txt

CMD ["python"]

