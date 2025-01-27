FROM python:3.11.9-slim AS builder

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install -y git gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . .
