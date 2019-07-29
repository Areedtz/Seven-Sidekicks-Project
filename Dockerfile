FROM tensorflow/tensorflow:2.0.0a0-gpu-py3

# Install apt dependencies
RUN apt-get update && \
    apt-get install -y wget libreadline-gplv2-dev libncursesw5-dev \
    libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz \
    && tar xf Python-3.6.8.tar.xz && cd Python-3.6.8 \
    && ./configure --enable-optimizations && make && make altinstall

RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py

# Compile, build and install the swig package
RUN apt-get update && \
    apt-get install -y git build-essential automake \
    libpcre3-dev autoconf libtool bison

RUN mkdir /swig && cd /swig && git clone https://github.com/swig/swig.git \
    && cd /swig/swig && ./autogen.sh && ./configure && make && make install \
    && cd / && rm -rf /swig

# Dependencies for the gaia package
RUN apt-get update && \
    apt-get install -y python2.7 python2.7-dev \
    libyaml-dev libqt4-dev

# Compile, build and install the gaia package
RUN mkdir /gaia && cd /gaia && git clone https://github.com/MTG/gaia.git \
    && cd /gaia/gaia && python2.7 waf configure --with-python-bindings \
    && python2.7 waf && python2.7 waf install && cd / && rm -rf /gaia

# Dependencies for the essentia package
RUN apt-get update && \
    apt-get install -y libfftw3-dev

# Compile, build and install the essentia package
RUN mkdir /essentia && cd /essentia && git clone https://github.com/MTG/essentia.git \
    && cd /essentia/essentia && git reset --hard 6b584720c2d0dc0202a9ed5fc4e2121756dadd3a \
    && python3.6 waf configure --build-static --with-examples --with-gaia \
    && python3.6 waf && python3.6 waf install && cd / && rm -rf /essentia

# Install cx_oracle requirements
RUN apt-get update && \
    apt-get install -y libaio-dev

ENV ORACLE_HOME /opt/oracle/instantclient_12_1
ENV LD_RUN_PATH $ORACLE_HOME
ENV LD_LIBRARY_PATH $ORACLE_HOME:$LD_LIBRARY_PATH

WORKDIR /tmp/

RUN wget https://github.com/odedlaz/docker-cx_oracle/raw/master/instantclient/instantclient-basic-linux.x64-12.1.0.2.0.zip
RUN wget https://github.com/odedlaz/docker-cx_oracle/raw/master/instantclient/instantclient-sdk-linux.x64-12.1.0.2.0.zip
RUN mkdir /opt/oracle/ && unzip "/tmp/instantclient*.zip" -d /opt/oracle
RUN ln -s $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/libclntsh.so
RUN mkdir $ORACLE_HOME/lib && cp $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/lib/libclntsh.so

# Install the clang compiler
RUN apt-get update && \
    apt-get install -y clang-6.0

# Set environment to use the clang compiler instead of gcc for use with pip
ENV CC=/usr/bin/clang-6.0

# Pip dependencies
RUN apt-get update && \
    apt-get install -y libmysqlclient-dev libpq-dev

COPY requirements.txt /requirements.txt
RUN pip3.6 install -r /requirements.txt && pip3.6 install essentia

RUN mkdir /code && chown 1000:1000 /code

WORKDIR /code

# librosa mp3 dependency
RUN apt-get update && \
    apt-get update && apt-get install -y ffmpeg

# Leftover packages from cleanup. Don't know if they're needed
RUN apt-get update \
    && apt-get install -y pkg-config libavcodec-dev libavformat-dev libavutil-dev \
    libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev

RUN apt-get update \
    && apt-get install -y python3-dev python3-numpy-dev python3-numpy python3-yaml \
    libncurses5-dev libreadline-dev liblzma-dev libffi-dev tcl-dev tk

# For live work
COPY src /code/