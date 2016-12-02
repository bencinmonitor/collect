# bencinmonitor / collect

Price collector and OCR for collected images.

## Setup

Prepare Python3 with virtualenv wrapper.

```bash
PYTHON_PATH=/usr/local/Cellar/python3/3.5.2_1/bin/python3
LDFLAGS="-L$(brew --prefix openssl)/lib"
CFLAGS="-I$(brew --prefix openssl)/include"
mkvirtualenv --no-site-packages --python=$PYTHON_PATH bm-collect
pip install --upgrade -r requirements.txt
```

## Crawling & Processing

```bash
redis-server ./etc/redis.conf

scrapy crawl petrol -L INFO
scrapy crawl omv -L INFO

python -m ocr_machine.workers default
```

## Notes

```bash
brew install opencv3 --HEAD --with-python3 --c++11 --with-contrib

ln -s /usr/local/opt/opencv3/lib/python3.5/site-packages/cv2.cpython-35m-darwin.so \
  /Users/otobrglez/.virtualenvs/bm-collect/lib/python3.5/site-packages/

pip install jupyter numpy matplotlib
```

# Docker

> In progress,...

```bash
docker build -t bencinmonitor/collect:latest .

docker-compose -f ./docker-compose.yml -f ./docker-compose.local.yml up

# docker run -ti -v `pwd`:/home/collect -p 6800:6800 bencinmonitor/collect /bin/bash -l
```

# Test suite

```bash
python -m unittest discover -s test
```

## Contributors

- [Oto Brglez](https://github.com/otobrglez)
