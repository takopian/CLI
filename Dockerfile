FROM python:3.8

WORKDIR /CLI

COPY requirements.txt .
COPY src/ ./src

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \

ENTRYPOINT bash