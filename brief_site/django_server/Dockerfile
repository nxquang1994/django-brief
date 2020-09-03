FROM python:3.7
ENV PYTHONUNBUFFERED 1

MAINTAINER test

RUN usermod -u 1000 www-data

RUN apt-get update \
  && apt-get install -y \
  default-mysql-client \
  locales

RUN echo en_US.UTF-8 UTF-8 > /etc/locale.gen
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD my.cnf /etc/mysql/conf.d/

RUN mkdir -p /server

ADD requirements.txt /server/

WORKDIR /server

RUN pip install -r requirements.txt

EXPOSE 8000
