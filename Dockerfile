FROM python:3.8-alpine

WORKDIR var/app/

RUN apk add --update curl gcc g++ python3-dev \
     musl-dev mariadb-dev tzdata\
 && rm -rf /var/cache/apk/*

COPY ./pyproject.toml ./poetry.lock* /var/app/

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | \
     POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install

COPY . /var/app

ENV PYTHONPATH=/var/app
