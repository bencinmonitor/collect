import scrapy


class CollectorSpider(scrapy.Spider):
    mode = 'refresh'
    over_pages = None
    over_categories = None

    def __init__(self, mode='refresh', pages=None, categories=None, *args, **kwargs):
        super(CollectorSpider, self).__init__(*args, **kwargs)
        self.mode = mode
