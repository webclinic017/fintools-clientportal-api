FROM python:alpine
WORKDIR /app
RUN apk add curl git
COPY requirements.py .
RUN pip install -r requirements.py
