FROM python:3.6

# Dependencies for the swig package
RUN apt-get update && \
    apt-get install -y bison

# Compile, build and install the swig package
WORKDIR /tmp/

RUN wget https://github.com/swig/swig/archive/rel-4.0.0.zip && unzip rel-4.0.0.zip \
    && cd swig-rel-4.0.0 && ./autogen.sh && ./configure && make && make install \
    && cd .. && rm -rf *rel-4.0.0*

# Dependencies for the gaia package
RUN apt-get update && \
    apt-get install -y python2.7-dev libqt4-dev

# Compile, build and install the gaia package
WORKDIR /tmp/

RUN wget https://github.com/MTG/gaia/archive/v2.4.5.zip && unzip v2.4.5.zip \
    && cd gaia-2.4.5 && python2.7 waf configure --with-python-bindings \
    && python2.7 waf && python2.7 waf install && cd .. && rm -rf *2.4.5*

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
RUN mkdir /opt/oracle/ && unzip "/tmp/instantclient*.zip" -d /opt/oracle && rm -rf instantclient*.zip
RUN ln -s $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/libclntsh.so
RUN mkdir $ORACLE_HOME/lib && cp $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/lib/libclntsh.so

# Install the clang compiler
RUN apt-get update && \
    apt-get install -y clang-6.0

# Set environment to use the clang compiler instead of gcc for use with pip
ENV CC=/usr/bin/clang-6.0

COPY requirements.txt /requirements.txt
RUN pip3.6 install -r /requirements.txt && pip3.6 install essentia

RUN mkdir /code && chown 1000:1000 /code

WORKDIR /code

# librosa mp3 dependency
RUN apt-get update && \
    apt-get update && apt-get install -y ffmpeg

# Leftover packages from cleanup. Don't know if they're needed
RUN apt-get update \
    && apt-get install -y libavcodec-dev libavformat-dev libavutil-dev \
    libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev

RUN apt-get update \
    && apt-get install -y python3-dev python3-numpy-dev \
    python3-numpy python3-yaml libffi-dev

# For live work
COPY src/ /code/
