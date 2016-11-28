# -*- coding: utf-8 -*-
from os import getenv

BOT_NAME = 'collector'
SPIDER_MODULES = ['collector.spiders']
NEWSPIDER_MODULE = 'collector.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'startproject (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = int(getenv("CONCURRENT_REQUESTS", "8"))

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = int(getenv("DOWNLOAD_DELAY", "2"))
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOAD_TIMEOUT = 30

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
COOKIES_DEBUG = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'startproject.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'startproject.middlewares.MyCustomDownloaderMiddleware': 543,
# }


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html

EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    # 'feeder.extensions.stats.DatadogStats': 500
}

ITEM_PIPELINES = {
    #    'startproject.pipelines.SomePipeline': 300,
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    # 'feeder.pipelines.FilesPipeline': 1,
    # 'scrapy.pipelines.files.FilesPipeline': 1,
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'collector.pipelines.StationsKafkaPipeline': 2
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = False
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Images
IMAGES_STORE = "data"

# Kafka
KAFKA_BOOTSTRAP_SERVERS = getenv('KAFKA_BOOTSTRAP_SERVERS', None)
KAFKA_SCRAPED_ITEMS_TOPIC = getenv('KAFKA_SCRAPED_ITEMS_TOPIC', 'scraped-items')
