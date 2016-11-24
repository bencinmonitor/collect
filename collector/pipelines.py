# -*- coding: utf-8 -*-
import hashlib
import os
import os.path
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from collector.settings import *


class StationsPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):

        if item.get('images'):
            item['images'] = [i['path'] for i in item.get('images')]

        if item.get('files'):
            item['files'] = [i['path'] for i in item.get('files')]

        return item


def custom_file_path(self, request, response=None, info=None):
    url = '' + request.url
    media_guid = hashlib.sha256(url.encode('utf-8')).hexdigest()

    media_ext = os.path.splitext(url)[1]

    if not media_ext[1:].isalpha():
        media_base_url = url.split('?', 1)[0]
        media_ext = os.path.splitext(media_base_url)[1]
        if media_ext == '.php':
            media_ext += '.pdf'

    return '%s%s' % (media_guid, media_ext)


FilesPipeline.file_path = custom_file_path
