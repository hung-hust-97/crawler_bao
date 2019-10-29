from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler_express.items import VnexpressCrawlerItem
from scrapy.exceptions import CloseSpider
import os



class VnexpressSpider(CrawlSpider):
    name = 'vnexpressSpider'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/the-gioi']
    with open("link_crawl.txt", "r") as f:
        for line in f.readlines():
            start_urls.append(line.strip())
    f.close()
    print(start_urls)
    MAX = 30000
    count = 0
    rules = (Rule(LinkExtractor(restrict_xpaths=('//*[@class= "next"]'), deny=('\S+p300')),callback="parse_items",follow= True),)

    def parse_items(self, response):
        with open('test.html', 'w') as f:
            f.write(str(response.body))
        urls = response.xpath('//*[@class="title_news"]/a[1]/@href')
        for url in urls:
            connect_url = response.urljoin(url.extract())
            yield Request(connect_url, callback= self.parse_question)


    def parse_question(self, response):
        item = VnexpressCrawlerItem()
        self.count += 1
        print(self.count)
        contents = response.xpath('//*[@class="content_detail fck_detail width_common block_ads_connect"]/p/text()').extract()
        contents = [content.strip() for content in contents]
        # if (contents == None):
        #     yield None
        item['content']     = " ".join(contents)
        if (item['content'] == "Video:"):
            yield None
        item['url']         = response.url
        item['title']       = response.xpath('//*[@class= "title_news_detail mb10"]/text()').extract_first().strip()
        item['time']        = response.xpath('//*[@class = "time left" ]/text()').extract_first()
        item['description'] = response.xpath('//*[@itemprop = "description" ]/@content').extract_first()
        item['keywords']    = response.xpath('//*[@name = "keywords"]/@content').extract_first()
        item['author']      = response.xpath('//*[@style="text-align:right;"]/strong/text()').extract_first()
        if (item['author'] == None):
            item['author'] = response.xpath('//*[@class="Normal"]/strong/text()').extract_first()
        if (item['author'] == None):
            item['author'] = response.xpath('//*[@class="author_mail"]/strong/text()').extract_first()
        item['topic']       = response.xpath('//*[@class="start"]/h4/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag_item"]/text()').extract()
        tags = [tag.strip()for tag in tags]
        item['tags'] = tags
        yield item