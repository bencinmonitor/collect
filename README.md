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

## Crawling

```bash
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties; \
kafka-server-start /usr/local/etc/kafka/server.properties

afka-topics --create --zookeeper localhost:2181 \
  --replication-factor 1 --partitions 1 --topic scraped-items

kafka-console-consumer --bootstrap-server localhost:9092 --topic \
  scraped-items --from-beginning

scrapy crawl petrol -L INFO
scrapy crawl omv -L INFO
```

## OCR

By default OCR machine listens to `scraped-items` topic.

```bash
./ocr-machine.sh
```

For OCR development this also works.

```bash
./ocr-machine.sh --image ./data-test/petrol.jpg
```

## Exploring

- [Exploring OCR (notebook)](explore/exploring-images-v2.ipynb)

```bash
brew install opencv3 --HEAD --with-python3 --c++11 --with-contrib

ln -s /usr/local/opt/opencv3/lib/python3.5/site-packages/cv2.cpython-35m-darwin.so \
  /Users/otobrglez/.virtualenvs/bm-collect/lib/python3.5/site-packages/

pip install jupyter numpy matplotlib
```


## Contributors

- [Oto Brglez](https://github.com/otobrglez)
