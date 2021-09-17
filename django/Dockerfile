FROM python:3.8-buster

ENV PYTHONUNBUFFERD 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /django

RUN adduser --disabled-password --gecos "" user

USER user
ENV PATH $PATH:/home/user/.local/bin


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /django
