FROM python:3.8-alpine

ARG DEPLOY_ENV
ENV DEPLOY_ENV ${DEPLOY_ENV}

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD python app.py
