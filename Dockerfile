FROM python:3.8

WORKDIR /CLI

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENTRYPOINT python /CLI/src/app.py
# ENTRYPOINT bash
