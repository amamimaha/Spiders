import scrapy


class wikitn(scrapy.Spider):
    name = "wikitn"

    def start_requests(self):
        urls = [
            'https://www.wiki.tn/pc-portable/pc-portable-vegabook-10-quad-core-2go-32-go-gold-white-8524.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'www.wiki.tn/-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)