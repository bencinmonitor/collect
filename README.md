# bencinmonitor / collect

Oil and gas price collector.

# Running with Docker

```bash
docker build -t bencinmonitor/collect:latest .

docker-compose -f docker-compose.yml -f docker-compose.local.yml up
```

## Local setuo notes

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
