# -*- coding: utf-8 -*-
from collector.spiders import CollectorSpider
from collector.items import Station
from scrapy import Request
from datetime import datetime
import sys
from scrapy import crawler
from slugify import slugify
import re


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
            'scraped_at': datetime.utcnow(),
            'scraped_url': response.url,
            'xid': str(response.url.split('/')[-1]),
            'xcode': response.xpath("//span[contains(@class,'oem')]/text()").extract()[0].split(" ")[-1],
            'name': response.css("h1.page-title::text").extract()[0],
            'address': response.css("span.address::text").extract()[0],
            'scraper': self.name
        })

        station['key'] = "%s-%s-%s" % (self.name, station['xid'], station['xcode'])

        prices_image = "//div[contains(@id, 'bsDetails')]" \
                       "//img[contains(@src,'files')]" \
                       "/@src"

        station['image_urls'] = ["%s%s" % (self.base_url, src) for src in
                                 response.xpath(prices_image).extract()]

        station['lat'], station['lon'] = [float(x.split(' ')[-1]) for x in
                                          response.xpath("//div[contains(@id,'qr-popup')]//p/text()").extract()]

        raw_services = response.css(".section.gs-offers h4::text").extract()
        station['services'] = {slugify(text, separator="_"): 1 for text in raw_services}
        station['services_humans'] = {slugify(text, separator="_"): text for text in raw_services}

        try:
            # non-stop
            station['shopping_hours'] = {
                'monday': {'open': 1, 'close': 2400},
                'tuesday': {'open': 1, 'close': 2400},
                'wednesday': {'open': 1, 'close': 2400},
                'thursday': {'open': 1, 'close': 2400},
                'friday': {'open': 1, 'close': 2400},
                'saturday': {'open': 1, 'close': 2400},
                'sunday': {'open': 1, 'close': 2400},
            }

            raw_times = [item for item in response.css(".opening-time dd::text").extract()]
            keys = [slugify(t, separator="_") for i, t in enumerate(raw_times) if (i % 2 == 0)]
            human_keys = [t for i, t in enumerate(raw_times) if (i % 2 == 0)]
            values = [t for i, t in enumerate(raw_times) if (i % 2 != 0)]
            raw_shopping = dict(zip(keys, values))
            station['shopping_hours_humans'] = dict(zip(human_keys, values))

            if raw_shopping.get('odprto', None) == 'NON-STOP':
                pass
            else:
                every_day = raw_shopping.get('vsak_delavnik', None)
                if every_day is not None:
                    every_day_range = self.parse_time_range(every_day)
                    for d in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                        station['shopping_hours'][d] = every_day_range

                sunday = raw_shopping.get('nedelje_in_prazniki', None)
                if sunday is not None: station['shopping_hours']['sunday'] = self.parse_time_range(sunday)

                saturday = raw_shopping.get('sobote', None)
                if saturday is not None: station['shopping_hours']['saturday'] = self.parse_time_range(saturday)

        except:
            station['shopping_hours'] = {}
            station['shopping_hours_humans'] = {}

        return station

    def parse_time_range(self, text):
        text = text.replace(":", "")
        times = list(map(int, re.findall('\d+', text)))
        return {'open': times[0], 'close': times[1]}
