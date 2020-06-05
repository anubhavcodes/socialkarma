FROM python:3.7-slim-buster

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esra \
 && rm -fr /var/lib/apt/lists/* \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

WORKDIR /srv

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV TWITTER_HANDLE=$TWITTER_HANDLE
ENV MONGO_URL=$MONGO_URL
ENV MONGO_DB=$MONGO_DB
ENV KEYBASE_HANDLE=$KEYBASE_HANDLE
ENV GITHUB_USERNAME=$GITHUB_USERNAME
ENV STACKOVERFLOW_HANDLE=$STACKOVERFLOW_HANDLE
ENV LINKEDIN_PROFILE_HANDLE=$LINKEDIN_PROFILE_HANDLE
ENV LINKEDIN_USERNAME=$LINKEDIN_USERNAME
ENV LINKEDIN_PASSWORD=$LINKEDIN_PASSWORD

COPY . .
