FROM python:3.10.9

COPY . /app
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN rm -rf python-poetry-buildpack && \
    git clone https://github.com/zensum/python-poetry-buildpack.git

RUN rm -rf /app/requirements.txt /app/runtime.txt
ENV POETRY_VERSION=1.1.15
RUN python-poetry-buildpack/bin/compile /app _ /app

RUN apt-get update && apt-get install -y "python$(cat app/runtime.txt | sed 's/python-//' | sed 's/\(.*\)\.[0-9]/\1/')"
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install debugpy "watchdog[watchmedo]"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app

CMD uvicorn main:app --reload --host 0.0.0.0 --port $PORT
