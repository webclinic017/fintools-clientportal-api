#!/usr/bin/env python3
# Taken from https://en.wikipedia.org/wiki/Flask_(web_framework)
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()
