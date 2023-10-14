FROM python:3.12.0-bookworm

RUN apt-get update

RUN pip install django

CMD tail -f /dev/null
