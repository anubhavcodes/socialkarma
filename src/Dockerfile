FROM python:3.7-slim-buster

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr \
 && rm -fr /var/lib/apt/lists/* \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

WORKDIR /srv

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
