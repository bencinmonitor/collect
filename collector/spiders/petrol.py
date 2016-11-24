# -*- coding: utf-8 -*-
from collector.spiders import CollectorSpider
from collector.items import Station
from scrapy import Request
from arrow import utcnow as scraped_at


class Petrol(CollectorSpider):
    name = 'petrol'
    base_url = "http://www.petrol.si"
    allowed_domains = ["petrol.si"]

    def start_requests(self):
        return [Request("%s/bencinski-servisi/seznam" % self.base_url)]

    def parse(self, response):
        if '/seznam' in response.url:
            return self.parse_list(response)
        elif '/podrobno' in response.url:
            return self.parse_detail(response)
        else:
            raise Exception("Sorry, can't parse %s" % response.url)

    def parse_list(self, response):
        slovenian_stations = "//div[contains(@class,'view-gas-station-list')]" \
                             "/div[contains(@class,'views-row')][position()<4]" \
                             "//td[contains(@class,'views-field-title')]" \
                             "/a/@href"

        return (Request(url="%s%s" % (self.base_url, href)) for href in
                response.selector.xpath(slovenian_stations).extract())

    def parse_detail(self, response):
        station = Station(**{
            'scraped_at': scraped_at(),
            'scraped_url': response.url,
            'xid': str(response.url.split('/')[-1]),
            'xcode': response.xpath("//span[contains(@class,'oem')]/text()").extract()[0].split(" ")[-1],
            'name': response.css("h1.page-title::text").extract()[0],
            'address': response.css("span.address::text").extract()[0]
        })

        prices_image = "//div[contains(@id, 'bsDetails')]" \
                       "//img[contains(@src,'files')]" \
                       "/@src"

        station['image_urls'] = ["%s%s" % (self.base_url, src) for src in
                                 response.xpath(prices_image).extract()]

        station['lat'], station['lon'] = [float(x.split(' ')[-1]) for x in
                                          response.xpath("//div[contains(@id,'qr-popup')]//p/text()").extract()]

        return station
