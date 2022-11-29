FROM ubuntu:22.04

WORKDIR /src

USER root

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get upgrade -y && \
    apt install software-properties-common -y && add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update
RUN apt install python3.8 python3.8-dev python3.8-venv python3.8-distutils python3.8-lib2to3 python3.8-gdbm python3.8-tk -y
RUN python3.8 -m venv /venv-cc
RUN /venv-cc/bin/python3.8 -m pip install --upgrade pip
COPY src/requirements.txt requirements.txt
RUN /venv-cc/bin/python3.8 -m pip install -r requirements.txt
RUN apt install make

COPY /src/envfile.env envfile.env
RUN export $(cat envfile.env | xargs)

COPY . .
COPY makefile makefile

CMD [ "make", "tests"]