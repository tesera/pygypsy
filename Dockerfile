FROM python:2.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    python-pip \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "docker@gypsy" && git config --global user.name "docker"

ENV WD=/opt/gypsy
WORKDIR /opt/gypsy
ENV HISTFILE $WD/.bash_history

RUN pip install virtualenv \
    && virtualenv -p python2.7 venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install numpy==1.11.2 \
    && pip install cython==0.25.1

COPY . /opt/gypsy

RUN pip install --upgrade -e .[docs,lint,test]
