FROM python:3.8-alpine

ARG DEPLOY_ENV
ENV DEPLOY_ENV ${DEPLOY_ENV}

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD python app.py