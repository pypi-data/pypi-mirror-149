apt-get upgrade -y
apt-get update -y


curl 'https://gitcode.net/q924257/mediapipe-title/-/raw/master/mediapipe-0.8-cp39-cp39-linux_aarch64.whl' -O -#

pip3 install mediapipe-0.8-cp39-cp39-linux_aarch64.whl -i https://pypi.tuna.tsinghua.edu.cn/simple

rm -f mediapipe-0.8-cp39-cp39-linux_aarch64.whl
