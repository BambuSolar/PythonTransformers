FROM caballerojavier13/python_transformers_base:latest

MAINTAINER Javier Caballero <caballerojavier13@gmail.com>

RUN mkdir /opt/page_crawler_bambu

ADD . /opt/python_transformers

ENV HOME /opt/python_transformers

WORKDIR /opt/python_transformers

RUN pip3 install -r requirements.txt

CMD eval "$(ssh-agent -s)"

CMD ssh-add /root/.ssh/id_rsa

CMD python3 app/transformers_server.py

EXPOSE 5000
