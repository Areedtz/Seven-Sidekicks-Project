FROM tensorflow/tensorflow:2.0.0a0-gpu-py3

# Install apt dependencies
RUN apt-get update \
    && apt-get install -y git build-essential libqt4-dev libyaml-dev \
    pkg-config libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev \
    libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev

RUN apt-get install -y python-six python3-dev python3-numpy-dev python3-numpy python3-yaml \
    autoconf automake cmake bison libpcre3-dev wget openssl libssl-dev zlib1g-dev \
    libncurses5-dev libreadline-dev libgdbm-dev libdb5.3-dev libbz2-dev liblzma-dev \
    libsqlite3-dev libffi-dev tcl-dev tk tk-dev
    
RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz \
    && tar xf Python-3.6.8.tar.xz && cd Python-3.6.8 \
    && ./configure --enable-optimizations && make && make altinstall

RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py

# Compile, build and install the swig package
RUN mkdir /swig && cd /swig && git clone https://github.com/swig/swig.git \
    && cd /swig/swig && ./autogen.sh && ./configure && make && make install \
    && cd / && rm -rf /swig

RUN mkdir /gaia && cd /gaia && git clone https://github.com/MTG/gaia.git \
    && cd /gaia/gaia && python2 waf configure --with-python-bindings \
    && python2 waf && python2 waf install && cd / && rm -rf /gaia

RUN mkdir /essentia && cd /essentia && git clone https://github.com/MTG/essentia.git \
    && cd /essentia/essentia && git reset --hard 6b584720c2d0dc0202a9ed5fc4e2121756dadd3a \
    && python3.6 waf configure --build-static --with-examples --with-gaia \
    && python3.6 waf && python3.6 waf install && cd / && rm -rf /essentia

COPY requirements.txt /requirements.txt
RUN pip3.6 install -r /requirements.txt && pip3.6 install essentia

RUN mkdir /code && chown 1000:1000 /code
WORKDIR /code