import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = [
        'http://example.com',
    ]

    def parse(self, response):
        self.log('Visited: %s' % response.url)