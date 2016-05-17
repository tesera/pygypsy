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

# Setting these environment variables are the same as running
# source /opt/learn/venv/bin/activate.
# ENV VIRTUAL_ENV /opt/gypsy/venv
# ENV PATH /opt/gypsy/venv/bin:$PATH
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --upgrade .[test]
