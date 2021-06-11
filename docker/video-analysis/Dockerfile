FROM tensorflow/tensorflow:2.0.0a0-gpu-py3

# Install apt dependencies
RUN apt-get update && \
    apt-get install -y wget libreadline-gplv2-dev libncursesw5-dev \
    libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz \
    && tar xf Python-3.6.8.tar.xz && cd Python-3.6.8 \
    && ./configure --enable-optimizations && make && make altinstall

RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py

# Install the clang compiler
RUN apt-get update && \
    apt-get install -y clang-6.0

# Set environment to use the clang compiler instead of gcc for use with pip
ENV CC=/usr/bin/clang-6.0

# Pip dependencies
RUN apt-get update && \
    apt-get install -y libmysqlclient-dev libpq-dev

COPY requirements.txt /requirements.txt
RUN pip3.6 install -r /requirements.txt

RUN mkdir /code && chown 1000:1000 /code

WORKDIR /code

# librosa mp3 dependency
RUN apt-get update && \
    apt-get install -y ffmpeg

# Leftover packages from cleanup. Don't know if they're needed
RUN apt-get update && \
    apt-get install -y libavcodec-dev libavformat-dev libavutil-dev \
    libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev

RUN apt-get update && \
    apt-get install -y python3-numpy-dev python3-numpy python3-yaml \
    libncurses5-dev libreadline-dev liblzma-dev

# For live work
COPY src/ /code/
