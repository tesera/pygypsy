FROM python:2.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    python-pip \
&& apt-get clean \
&& apt-get autoclean \
&& rm -rf /var/lib/apt/lists/*

ENV WD=/opt/gypsy
COPY . /opt/gypsy
WORKDIR /opt/gypsy

RUN pip install virtualenv
RUN virtualenv -p python2.7 venv

RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --upgrade .[test]
