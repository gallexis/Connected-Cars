#Install dependencies

sudo apt-get update
sudo apt-get upgrade
sudo rpi-update

sudo reboot

sudo apt-get install build-essential git cmake pkg-config

sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev

sudo apt-get install libgtk2.0-dev

sudo apt-get install libatlas-base-dev gfortran

sudo apt-get install python2.7-dev python3-dev

#Grab the OpenCV source code

cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.0.0.zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.0.0.zip
unzip opencv_contrib.zip


#Setup Python

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

source ~/.profile

mkvirtualenv cv

mkvirtualenv cv -p python3

source ~/.profile
workon cv

pip install numpy


#Compile and install OpenCV

workon cv

cd ~/opencv-3.0.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.0.0/modules \
	-D BUILD_EXAMPLES=ON ..


make -j4

make clean
make

sudo make install
sudo ldconfig

ls -l /usr/local/lib/python2.7/site-packages/
total 1636
-rw-r--r-- 1 root staff 1675144 Oct 17 15:25 cv2.so

cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so

ls /usr/local/lib/python3.4/site-packages/
cv2.cpython-34m.so

cd /usr/local/lib/python3.4/site-packages/
sudo mv cv2.cpython-34m.so cv2.so

cd ~/.virtualenvs/cv/lib/python3.4/site-packages/
ln -s /usr/local/lib/python3.4/site-packages/cv2.so cv2.so

#Verifying your OpenCV 3 install

workon cv
python
>>> import cv2
>>> cv2.__version__
'3.0.0'


