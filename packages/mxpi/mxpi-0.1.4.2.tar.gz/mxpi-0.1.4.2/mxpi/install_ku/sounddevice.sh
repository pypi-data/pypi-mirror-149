apt-get upgrade -y
apt-get update -y

apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y

pip3 install pyaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install SoundFile -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install sounddevice -i https://pypi.tuna.tsinghua.edu.cn/simple

