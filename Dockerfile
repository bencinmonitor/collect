FROM ubuntu:16.04

MAINTAINER Oto Brglez <otobrglez@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8 \
  LANGUAGE=C.UTF-8

RUN apt-get update -qy && \
  apt-get install -qy \
  libssl-dev libffi-dev \
  zlib1g-dev libjpeg-dev libtiff-dev libpng-dev libtiff-dev libicu-dev libjasper-dev \
  python3 python3-pip python3-setuptools python3-cffi python3-numpy \
  tesseract-ocr libtesseract-dev libleptonica-dev tesseract-ocr-dev \
  tesseract-ocr-slv tesseract-ocr-eng && \
  update-alternatives --install /usr/bin/python python /usr/bin/python3 10 && \
  update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

# Setup OpenCV2
ADD ./lib/libopencv.tar.gz /tmp/
RUN cp --no-dereference /tmp/libopencv/lib* /usr/local/lib/ && \
  cp /tmp/libopencv/python*/* /usr/local/lib/python3.5/dist-packages/ && \
  ldconfig

RUN mkdir -p /home/collect/data/full

ADD . /home/collect

# Project Python dependencies
RUN pip install --disable-pip-version-check Cython==0.24 && \
  pip install --no-binary --no-use-wheel --no-cache-dir --disable-pip-version-check \
  -r /home/collect/requirements.txt

WORKDIR /home/collect

VOLUME /home/collect/data/full

RUN apt-get clean && apt-get purge -y --auto-remove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["scrapy"]