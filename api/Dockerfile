FROM python:alpine
WORKDIR /app
COPY requirements.py .
RUN pip install -r requirements.py
RUN apk add curl
