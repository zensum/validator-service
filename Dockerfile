FROM python:3.9

COPY . /app
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes
RUN pip install -r requirements.txt
RUN pip install debugpy

ENV FLASK_APP debugger.py

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app

CMD PORT=80 python main.py
