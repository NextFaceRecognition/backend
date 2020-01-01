FROM python:3.6-slim-stretch

RUN echo "deb http://mirrors.aliyun.com/debian stretch main contrib non-free
deb http://mirrors.aliyun.com/debian stretch-proposed-updates main contrib non-free
deb http://mirrors.aliyun.com/debian stretch-updates main contrib non-free
deb-src http://mirrors.aliyun.com/debian stretch main contrib non-free
deb-src http://mirrors.aliyun.com/debian stretch-proposed-updates main contrib non-free
deb-src http://mirrors.aliyun.com/debian stretch-updates main contrib non-free
deb http://mirrors.aliyun.com/debian-security/ stretch/updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian-security/ stretch/updates main non-free contrib
deb http://mirrors.aliyuncs.com/debian stretch main contrib non-free
deb http://mirrors.aliyuncs.com/debian stretch-proposed-updates main contrib non-free
deb http://mirrors.aliyuncs.com/debian stretch-updates main contrib non-free
deb-src http://mirrors.aliyuncs.com/debian stretch main contrib non-free
deb-src http://mirrors.aliyuncs.com/debian stretch-proposed-updates main contrib non-free
deb-src http://mirrors.aliyuncs.com/debian stretch-updates main contrib non-free
deb http://mirrors.aliyuncs.com/debian-security/ stretch/updates main non-free contrib
deb-src http://mirrors.aliyuncs.com/debian-security/ stretch/updates main non-free contrib" > /etc/apt/source.list

RUN apt-get clean
RUN apt-get -y update

RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

COPY . /root/face_recognition_server
RUN cd /root/face_recognition_server && \
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

