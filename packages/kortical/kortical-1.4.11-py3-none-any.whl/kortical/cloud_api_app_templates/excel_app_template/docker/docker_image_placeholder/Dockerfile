# syntax=docker/dockerfile:experimental
FROM python:3.8-slim as compile

ENV LANG=en_GB.UTF-8
ENV LC_ALL=en_GB.UTF-8
ENV PYTHONUNBUFFERED=1

# Install the least frequently changing things
RUN python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools && \
    mkdir -p /opt/kortical-cloud/venvs && \
    python3 -m venv /opt/kortical-cloud/venvs/app-venv

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=$HOME/.cache/pip --mount=type=ssh \
    apt-get update && \
    apt-get install ssh -y && \
    apt-get install dos2unix -y  && \
    mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts && \
    apt-get install gcc git git-core -y && \
    . /opt/kortical-cloud/venvs/app-venv/bin/activate && \
    pip install cryptography==2.9 gitpython==3.1.24 gitdb==4.0.7 setuptools==51.1.1

# Next install the pip requirements
ADD requirements.txt /data/requirements.txt
ADD docker/docker_image_placeholder/run-cmd.sh /usr/local/bin/run-cmd.sh

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    dos2unix /usr/local/bin/run-cmd.sh && \
    dos2unix /data/requirements.txt && \
    . /opt/kortical-cloud/venvs/app-venv/bin/activate && \
    pip install -r /data/requirements.txt

# Lastly copy over the data and the code and install the package
ADD setup.py /data/app_name_placeholder/setup.py
ADD pytest.ini /data/app_name_placeholder/pytest.ini
ADD src /data/app_name_placeholder/src

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=$HOME/.cache/pip --mount=type=ssh \
    find /data/app_name_placeholder -type f -print0 | xargs -0 dos2unix -- && \
    . /opt/kortical-cloud/venvs/app-venv/bin/activate && \
    pip install -e /data/app_name_placeholder

FROM python:3.8-slim

RUN groupadd korticalgroup && \
    useradd -ms /bin/bash kortical -g korticalgroup

COPY --from=compile --chown=kortical:korticalgroup /opt/kortical-cloud/venvs/app-venv /opt/kortical-cloud/venvs/app-venv/
COPY --from=compile --chown=kortical:korticalgroup /data/app_name_placeholder/src /data/app_name_placeholder/src/
COPY --from=compile --chown=kortical:korticalgroup /usr/local/bin/run-cmd.sh /usr/local/bin/run-cmd.sh

RUN chmod +x /usr/local/bin/run-cmd.sh

USER kortical