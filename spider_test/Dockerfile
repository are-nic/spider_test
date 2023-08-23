FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/spider_test

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./static

COPY . .