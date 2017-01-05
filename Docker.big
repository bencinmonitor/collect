FROM ubuntu:16.04

MAINTAINER Oto Brglez <otobrglez@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

RUN apt-get update -qq && \
  apt-get install -qqy \
  build-essential git pkg-config gcc g++ autoconf automake cmake libtool checkinstall libssl-dev libffi-dev \
  python3 python3-setuptools python3-dev python3-pip python3-cffi python3-numpy \
  zlib1g-dev libjpeg-dev libtiff-dev libpng-dev libtiff-dev libicu-dev libjasper-dev \
  tesseract-ocr libtesseract-dev libleptonica-dev tesseract-ocr-dev \
  tesseract-ocr-slv tesseract-ocr-eng \
  libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
  libblas-dev liblapack-dev

RUN mkdir -p /var/log/supervisor

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10 && \
  update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

RUN mkdir -p /src && cd /src/ && \
  git clone https://github.com/Itseez/opencv.git --depth 1 -b master && \
  cd /src/opencv/ && mkdir build && cd build && \
  cmake \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_DOCS=OFF \
    -D WITH_FFMPEG=OFF \
    .. && \
  make -j4 && make install && ldconfig

RUN mkdir -p /home/collect/data/full

ADD . /home/collect

# Project Python dependencies
RUN pip install --disable-pip-version-check Cython==0.24 && \
  pip install --no-binary --no-use-wheel --no-cache-dir --disable-pip-version-check \
  -r /home/collect/requirements.txt

RUN apt-get clean -qq && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# /src/opencv

WORKDIR /home/collect

VOLUME /home/collect/data/full

EXPOSE 6800

CMD ["/usr/local/bin/circusd", "/home/collect/etc/circusd.conf"]


