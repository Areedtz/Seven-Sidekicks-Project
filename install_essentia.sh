#!/usr/bin/env bash


# Install apt dependencies
echo "Installing apt dependencies..."
sudo apt-get update
sudo apt-get install -y build-essential libqt4-dev libyaml-dev pkg-config libyaml-dev

sudo apt-get install -y libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev
sudo apt-get install -y python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev python-six
sudo apt-get install -y python3-dev python3-numpy-dev python3-numpy python3-yaml

# Install Gaia2 if not already installed
if [ ! -d "/usr/local/include/gaia2" ]; then
    echo "Gaia not installed. Checking for swig..."

    # Install Swig if not already installed
    if [ ! -d "/usr/local/share/swig" ]; then
        echo "Swig not installed. Installing swig..."
        cd $HOME

        git clone https://github.com/swig/swig.git
        cd swig

        ./autogen.sh
        ./configure
        make
        sudo make install
    fi
    
    echo "Swig installed. Installing gaia..."
    cd $HOME

    git clone https://github.com/MTG/gaia/
    cd gaia

    python2 ./waf configure --with-python-bindings
    python2 ./waf
    sudo python2 ./waf install

    echo "Gaia installed."
fi

# Install Essentia if not already installed
if [ ! -d "/usr/local/include/essentia" ]; then
    echo "Essentia not installed. Installing Essentia..."
    cd $HOME

    wget https://github.com/MTG/essentia/archive/v2.1_beta4.zip
    unzip v.2.1_beta4.zip
    cd essentia-2.1_beta4

    ./waf configure --build-static --with-examples --with-python --with-gaia
    ./waf
    sudo python3 ./waf install

    python -c 'import essentia'
    echo "Essentia installed."
fi

echo "All dependencies successfully installed. Going to tests..."

cd $TRAVIS_BUILD_DIR