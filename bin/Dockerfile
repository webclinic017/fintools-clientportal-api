FROM python:alpine
WORKDIR /opt/fintools-ib
COPY requirements.py .
RUN apk add curl git jq
RUN pip install -r requirements.py
