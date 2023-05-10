FROM python:3.9-slim AS builder

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./ ./django_REST_vk_friends

RUN pip install gunicorn

ENV TZ Europe/Moscow

WORKDIR /django_REST_vk_friends
