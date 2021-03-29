#!/usr/bin/env bash

# Install apt dependencies
echo "Installing apt dependencies..."
sudo apt-get update > /dev/null && \
sudo apt-get install -y \
    build-essential libqt4-dev libyaml-dev pkg-config libyaml-dev \
    libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev \
    python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev python-six \
    python3-dev python3-numpy-dev python3-numpy python3-yaml > /dev/null

# Install Gaia2 if not already installed
if [ ! -d "/usr/local/include/gaia2" ]; then
    echo "Gaia not installed. Checking for swig..."

    # Install Swig if not already installed
    if [ ! -d "/usr/local/share/swig" ]; then
        echo "Swig not installed. Installing swig..."
        cd $HOME

        wget -q https://github.com/swig/swig/archive/rel-4.0.0.zip
        unzip rel-4.0.0.zip > /dev/null
        cd swig-rel-4.0.0

        ./autogen.sh > /dev/null
        ./configure > /dev/null
        make > /dev/null
        sudo make install /dev/null
        cd ..
        rm -rf *rel-4.0.0*
    fi
    
    echo "Swig installed. Installing gaia..."
    cd $HOME

    wget -q https://github.com/MTG/gaia/archive/v2.4.5.zip
    unzip v2.4.5.zip > /dev/null
    cd gaia-2.4.5

    python2 ./waf configure --with-python-bindings > /dev/null
    python2 ./waf > /dev/null
    sudo python2 ./waf install > /dev/null
    cd ..
    rm -rf *2.4.5

    echo "Gaia installed."
fi

# Install Essentia if not already installed
if [ ! -d "/home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/essentia/" ]; then
    echo "Essentia not installed. Installing Essentia..."
    cd $HOME

    git clone https://github.com/MTG/essentia >/dev/null
    cd essentia

    # As of the moment I'm making this commit (25/03/2019), their master doesn't work. This commit works.
    git reset --hard 6b584720c2d0dc0202a9ed5fc4e2121756dadd3a

    ./waf configure --build-static --with-examples --with-python --with-gaia > /dev/null
    ./waf > /dev/null
    sudo python3 ./waf install > /dev/null

    python -c 'import essentia'

    cd ..
    rm -rf essentia
    echo "Essentia installed."
fi

echo "All dependencies successfully installed. Going to tests..."

cd $TRAVIS_BUILD_DIR
mv config-travis.yml src/config.yml

cd src
