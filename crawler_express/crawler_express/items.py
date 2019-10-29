from scrapy.item import Item, Field

class VnexpressCrawlerItem(Item):
    title = Field()
    time = Field()
    content = Field()
    topic = Field()
    url = Field()
    tags = Field()
    description = Field()
    keywords = Field()
    author = Field()
class Bao24hCrawlerItem(Item):
    title = Field()
    time = Field()
    content = Field()
    topic = Field()
    url = Field()
    tags = Field()
    description = Field()
    keywords = Field()
    author = Field()