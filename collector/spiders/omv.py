# -*- coding: utf-8 -*-
from collector.spiders import CollectorSpider
from collector.items import Station
from scrapy import Request
from datetime import datetime
from json import loads


class OMV(CollectorSpider):
    name = 'omv'
    base_url = "https://www.omv.si"
    api_base_url = "https://webgispu.wigeogis.com"
    allowed_domains = ["omv.si", "wigeogis.com"]

    def start_requests(self):
        base_api_url = "%s/kunden/omvpetrom/backend/getFsForCountry.php?CTRISO=SVN" % self.api_base_url
        return [Request(base_api_url)]

    def parse(self, response):
        if '/getFsForCountry' in response.url:
            return self.parse_list(response)
        if '/details' in response.url:
            return self.parse_detail(response)
        else:
            raise Exception("Sorry, can't parse %s" % response.url)

    def parse_list(self, response):
        details_api_url = "%s/kunden/omvpetrom/client/details.php?LNG=SI&CTRISO=SVN&BRAND=OMV&ID=%s"
        return (Request(url=details_api_url % (self.api_base_url, record['sid']),
                        meta={'record': record}) for record in
                loads(response.body_as_unicode(), 'utf-8')['results'])

    def parse_detail(self, response):
        record = response.meta.get('record', {})
        name = "%s %s" % (record['brand_id'], record['address_l'])
        address = "%s, %s %s, %s" % (record['address_l'], record['postcode'], record['town_l'], record['country_l'])

        return Station(**{
            'scraped_at': datetime.utcnow(),
            'scraped_url': response.url,
            'xid': record['sid'],
            'xcode': record['sid'],
            'lat': record['y'],
            'lon': record['x'],
            'name': name,
            'address': address,
            'image_urls': response.xpath("//img[contains(@class,'preisImageClass')]/@src").extract(),
            'key': "%s-%s" % (self.name, record['sid']),
            'scraper': self.name
        })
