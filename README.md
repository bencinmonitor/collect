# bencinmonitor / collect

Oil and gas price collector.

[![Build Status](https://travis-ci.org/bencinmonitor/collect.svg?branch=master)](https://travis-ci.org/bencinmonitor/collect)

# Running with Docker

```bash
docker build -t bencinmonitor/collect:latest .

docker-compose -f docker-compose.yml -f docker-compose.local.yml up
```

## Development with Docker

```bash
docker-compose -f ./docker-compose.yml -f ./docker-compose.test.yml up mongo redis

docker run -ti --rm  -v `pwd`:/home/collect --network collect_default \
  --link collect_mongo_1:mongo --link collect_redis_1:redis \
  --entrypoint python bencinmonitor/collect -m unittest
```

## Debugging with Docker and pydevd

```bash
sudo ifconfig lo0 alias 10.8.8.8 netmask 255.255.255.255 up

docker run --privileged --host net --...
```

```python
from pydevd import settrace
settrace('10.8.8.8', port=10000, stdoutToServer=True, stderrToServer=True)
```

## Local setup notes

Prepare Python3 with virtualenv wrapper.

```bash
PYTHON_PATH=/usr/local/Cellar/python3/3.5.2_1/bin/python3
LDFLAGS="-L$(brew --prefix openssl)/lib"
CFLAGS="-I$(brew --prefix openssl)/include"
mkvirtualenv --no-site-packages --python=$PYTHON_PATH bm-collect

pip install --upgrade -r requirements.txt

brew install opencv3 --HEAD --with-python3 --c++11 --with-contrib

ln -s /usr/local/opt/opencv3/lib/python3.5/site-packages/cv2.cpython-35m-darwin.so \
  /Users/otobrglez/.virtualenvs/bm-collect/lib/python3.5/site-packages/

pip install jupyter numpy matplotlib
```

# Test suite

```bash
python -m unittest discover -s test
```

## Contributors

- [Oto Brglez](https://github.com/otobrglez)
