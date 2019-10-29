from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler_express.items import Bao24hCrawlerItem
from scrapy.exceptions import CloseSpider
import os



class Bao24hSpider(CrawlSpider):
    name = 'Bao24hSpider'
    allowed_domains = ['www.24h.com.vn']
    start_urls = ['https://www.24h.com.vn/bong-da-c48.html']
    with open("link_crawl.txt", "r") as f:
        for line in f.readlines():
            start_urls.append(line.strip())
    f.close()
    print(start_urls)
    MAX = 30000
    count = 0
    rules = (Rule(LinkExtractor(restrict_xpaths=('//*[@class= "pgIt pgAt"]'), deny=('\S+vpage=400')),callback="parse_items",follow= True),)



    def parse_items(self, response):
        with open('test.html', 'w') as f:
            f.write(str(response.body))
        urls = response.xpath('//*[@class= "nwsTit postname"]/a/@href')
        for url in urls:
            connect_url = response.urljoin(url.extract())
            yield Request(connect_url, callback= self.parse_question)



    def parse_question(self, response):
        item = Bao24hCrawlerItem()
        self.count += 1
        print(self.count)
        contents = response.xpath('//*[@class="nwsHt nwsUpgrade"]/p[not(@class="img_chu_thich_0407")]/text()').extract()
        contents = [content.strip() for content in contents]
        item['content']     = " ".join(contents)
        if (item['content'] == None):
            yield None
        item['url']         = response.url
        item['title']       = response.xpath('//*[@itemprop = "headline"]/text()').extract_first()
        item['time']        = response.xpath('//*[@class = "updTm updTmD mrT5" ]/text()').extract_first()
        item['description'] = response.xpath('//*[@name = "description" ]/@content').extract_first()
        item['keywords']    = response.xpath('//*[@name = "keywords"]/@content').extract_first()
        item['author']      = response.xpath('//*[@class = "nguontin nguontinD bld mrT10 mrB10 fr"]/text()').extract_first().strip()
        item['topic']       = response.xpath('//*[@class="brmItem bld"]/span/text()').extract_first()
        tags = response.xpath('//*[@class="sbNws"]/h3/a/text()').extract()
        tags = [tag.strip()for tag in tags]
        item['tags'] = ", ".join(tags)
        self.count += 1
        if self.count > self.MAX:
            raise CloseSpider('30000 pages crawled')
        yield item