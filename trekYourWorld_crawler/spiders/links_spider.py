import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import signals

class LinksSpider(CrawlSpider):
    name = 'links_spider'
    links_array = []

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, url=None, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
            self.allowed_domains = [url.split("//")[-1].split("/")[0]]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LinksSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse_item(self, response):
        self.log(f'Found a link: {response.url}')
        self.links_array.append(response.url)

    def spider_closed(self, spider):
        print("Crawled links:")
        for link in self.links_array:
            print(link)

# Run the Spider with a URL from CLI
