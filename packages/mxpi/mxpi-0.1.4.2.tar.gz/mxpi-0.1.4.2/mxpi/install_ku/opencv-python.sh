apt-get upgrade -y
apt-get update -y

apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
apt-get -y install libxvidcore-dev libx264-dev
apt-get -y install qt4-dev-tools libatlas-base-dev

pip3 install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
