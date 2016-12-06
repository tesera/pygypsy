FROM python:2.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    python-pip \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "docker@pygypsy" && git config --global user.name "docker"

ENV WD=/opt/pygypsy
WORKDIR /opt/pygypsy
ENV HISTFILE $WD/.bash_history

RUN pip install virtualenv \
    && virtualenv -p python2.7 venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install numpy==1.11.2 cython==0.25.1 coveralls

COPY . /opt/pygypsy

RUN . venv/bin/activate \
    && pip install -e .[test,lint,docs,dev]
