# u3

## Setup

Prepare Python3 with virtualenv wrapper.

```bash
PYTHON_PATH=/usr/local/Cellar/python3/3.5.2_1/bin/python3
mkvirtualenv --no-site-packages --python=$PYTHON_PATH u3
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" \
  pip install --upgrade -r requirements.txt
```

## Contributors

- [Oto Brglez](https://github.com/otobrglez)
