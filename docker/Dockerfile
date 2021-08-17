FROM python:3.9.6

COPY . /app
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes --dev

RUN pip install -r requirements.txt

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app

CMD uvicorn main:app --reload --host 0.0.0.0 --port $PORT
