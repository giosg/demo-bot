FROM python:2

ADD . /srv

RUN pip install -r /srv/requirements.txt

WORKDIR /srv/