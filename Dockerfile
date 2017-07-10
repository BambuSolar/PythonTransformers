FROM python:3.5

MAINTAINER Javier Caballero <caballerojavier13@gmail.com>

ADD . /opt/python_transformers

ENV HOME /opt/python_transformers

WORKDIR /opt/python_transformers

RUN export LC_ALL=C

# RUN pip3 install -r requirements.txt

RUN apt-get update

RUN apt-get install virtualenv python-virtualenv

RUN apt-get install git

RUN cp id_rsa /root/.ssh/id_rsa

RUN eval "$(ssh-agent -s)"

RUN ssh-add /root/.ssh/id_rsa

RUN virtualenv venv

RUN source venv/bin/activate

CMD python3 app/transformers_server.py

EXPOSE 5000