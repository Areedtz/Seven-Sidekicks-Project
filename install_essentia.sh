#!/usr/bin/env bash

sudo apt-get install build-essential libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev python-dev libsamplerate0-dev libtag1-dev
sudo apt-get install python-numpy-dev python-numpy python-yaml git

git clone https://github.com/MTG/essentia

cd essentia
./waf configure --mode=release --with-python
./waf
sudo ./waf install

python -c 'import essentia'