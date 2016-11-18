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
    && pip install numpy==1.11.2 cython==0.25.1

COPY . /opt/gypsy

RUN . venv/bin/activate \
    && python setup.py bdist_wheel \
    && pip install dist/gypsy-0.0.1.dev0-cp27-cp27mu-linux_x86_64.whl[test,lint,docs]
