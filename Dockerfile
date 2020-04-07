FROM ubuntu:18.04

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox \
    python3 python3-pip \
 && rm -fr /var/lib/apt/lists/* \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

WORKDIR /srv

COPY requirements.txt .

RUN apt-get install -y --no-install-recommends python3-pip

RUN python3 -m pip install -r requirements.txt

COPY src .

CMD ["python3", "app.py"]
