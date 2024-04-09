FROM ubuntu:22.04 AS base

USER root

# coloring syntax for headers
ENV CYAN='\033[0;36m'
ENV CLEAR='\033[0m'
ENV DEBIAN_FRONTEND='noninteractive'

# setup ubuntu user
ARG UID_='1000'
ARG GID_='1000'
RUN echo "\n${CYAN}SETUP UBUNTU USER${CLEAR}"; \
    addgroup --gid $GID_ ubuntu && \
    adduser \
        --disabled-password \
        --gecos '' \
        --uid $UID_ \
        --gid $GID_ ubuntu
WORKDIR /home/ubuntu

# update ubuntu and install basic dependencies
RUN echo "\n${CYAN}INSTALL GENERIC DEPENDENCIES${CLEAR}"; \
    apt update && \
    apt install -y \
        software-properties-common \
        wget && \
    rm -rf /var/lib/apt/lists/*

# install python3.10 and pip
RUN echo "\n${CYAN}SETUP PYTHON3.10${CLEAR}"; \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install --fix-missing -y python3.10 && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.10 get-pip.py && \
    rm -rf /home/ubuntu/get-pip.py

# install f8s
USER ubuntu
ENV REPO='f8s'
ENV PYTHONPATH "${PYTHONPATH}:/home/ubuntu/$REPO/python"
ARG VERSION
RUN echo "\n${CYAN}INSTALL F8S{CLEAR}"; \
    pip3.10 install --user f8s==$VERSION

ENV PATH=$PATH:/home/ubuntu/.local/bin
EXPOSE 8080

# setup configmap and secrets
ENV DEMO_CONFIG_PATH=/home/ubuntu/f8s/demo-config.yaml
ENV DEMO_TOKEN=abcdefgh12345678
RUN echo "\n${CYAN}CREATE F8S CONFIG DIRECTORY${CLEAR}"; \
    mkdir /home/ubuntu/f8s

COPY --chown=ubuntu:ubuntu scripts/test_app.py /home/ubuntu/test_app.py
