#!/usr/bin/env bash

cd ..

# Install swig
git clone https://github.com/swig/swig.git
cd swig

./autogen.sh
./configure
make
sudo make install

cd ..

# Install gaia
sudo apt-get update
sudo apt-get install build-essential libqt4-dev libyaml-dev pkg-config

git clone https://github.com/MTG/gaia/
cd gaia

python2 ./waf configure --with-python-bindings
python2 ./waf
python2 ./waf install

cd ..

# Install essentia
sudo apt-get install libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev python-six
sudo apt-get install python3-dev python3-numpy-dev python3-numpy python3-yaml

git clone https://github.com/MTG/essentia
cd essentia

./waf configure --build-static --with-examples --with-python --with-gaia
./waf
./waf install

python -c 'import essentia'

cd ../Seven-Sidekicks-Project