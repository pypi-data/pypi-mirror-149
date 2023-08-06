apt-get upgrade -y
apt-get update -y


curl 'https://gitcode.net/q924257/tensorflow-bin/-/raw/master/tensorflow-2.8.0-cp39-none-linux_aarch64.whl' -O -#

pip3 install tensorflow-2.8.0-cp39-none-linux_aarch64.whl -i https://pypi.tuna.tsinghua.edu.cn/simple

rm -f tensorflow-2.8.0-cp39-none-linux_aarch64.whl
