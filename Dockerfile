# escape=\

FROM ubuntu:latest

RUN apt-get update

# install python
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y git

COPY . /BotManClient
WORKDIR /BotManClient
RUN python3 -m venv ./venv
RUN ./venv/bin/python3 -m ensurepip
RUN . venv/bin/activate && pip install -r requirements.txt
# install requirements

# Run
CMD . venv/bin/activate && exec ./venv/bin/python3 main.py
