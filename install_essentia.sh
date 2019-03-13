#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install build-essential libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev python-six
sudo apt-get install python3-dev python3-numpy-dev python3-numpy python3-yaml

git clone https://github.com/MTG/essentia

cd essentia
./waf configure --build-static --with-examples --with-python
./waf
./waf install

python -c 'import essentia'

cd ..