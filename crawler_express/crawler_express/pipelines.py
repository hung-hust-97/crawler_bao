from scrapy.exceptions import DropItem
from crawler_express.exporters import JsonItemExporter
import json
import codecs
from scrapy.exceptions import CloseSpider

class CrawlerBaoPipeline(object):
    def __init__(self):
        self.file = codecs.open("exporters.json", 'w', encoding="utf-8")

    def close_spider(self, spider):
        self.file.close()


    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        return item