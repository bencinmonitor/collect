FROM ubuntu:16.04

MAINTAINER Oto Brglez <otobrglez@gmail.com>

RUN apt-get update -qq && \
  apt-get install -qy \
  build-essential pkg-config gcc g++ autoconf automake libtool checkinstall libssl-dev libffi-dev \
  python3 python3-setuptools python3-dev python3-pip python3-cffi \
  zlib1g-dev libjpeg-dev libtiff-dev libpng-dev libtiff-dev libicu-dev \
  tesseract-ocr libtesseract-dev  libleptonica-dev tesseract-ocr-dev \
  tesseract-ocr-slv tesseract-ocr-eng

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10 && \
  update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

RUN mkdir -p /home/collect/data/full

ADD . /home/collect

RUN pip install Cython==0.24 && \
  pip install --no-binary --no-use-wheel --no-cache-dir -r /home/collect/requirements.txt

WORKDIR /home/collect

VOLUME /home/collect/data/full


