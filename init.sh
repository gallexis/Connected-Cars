#!/bin/bash


if [ $1 == "pc" ]
then
    echo "PC"

    sudo apt-get install -y \
    git \
    python-tk

else
    echo "Raspi"

    sudo apt-get install -y \
    python-dev \
    python-smbus \
    subversion \
    libv4l-dev \
    libjpeg8-dev \
    imagemagick

    sudo echo "#blacklist i2c-bcm2708" >> /etc/modprobe.d/raspi-blacklist.conf

    if grep -Fxq "i2c-dev" /etc/modules
    then
        echo "i2c-dev already in /etc/modules"
    else
        echo "Adding i2c-dev in /etc/modules"
        sudo echo "i2c-dev" >> /etc/modules
    fi

    sudo modprobe i2c_bcm2708
    sudo modprobe i2c-dev

    echo "i2c drivers: "
    lsmod | grep i2c

    #camera
    cd mjpg-streamer/mjpg-streamer/
    make USE_LIBV4L2=true clean all
    sudo make DESTDIR=/usr install
    sudo sh start.sh

    echo "Get the id & password then go to your browser"
    cd ../..

fi






