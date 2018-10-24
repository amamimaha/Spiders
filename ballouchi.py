from datetime import datetime
import scrapy
import csv
from elasticsearch import Elasticsearch


class QuotesSpider(scrapy.Spider):
    name = "ballouchi"
    timestamp =  str(datetime.now())
    def start_requests(self):

        urls =[
        'https://www.ballouchi.com/annonces/vehicules/voitures/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse(self, response):
        #print(response.xpath("//h1[@itemprop='name']/text()").extract_first(),"*****************")
        el_cnx=Elasticsearch('localhost:9200',timeout=3000.0)
        Price = response.xpath("//span[@itemprop='price']/text()").extract_first()
        print
        Price_corrected = Price.replace('TND','')
        Price_without_space = int(Price_corrected.replace(' ',''))
        print(Price_without_space,"**********************")
        article =  {
                #'Annonce': response.xpath("//h1[@itemprop='name']/text()").extract_first(),
                'Model': response.xpath("//span[@itemprop='brand']/text()").extract_first(),
                'CirculationDate': response.xpath("//span[@itemprop='vehicleModelDate']/text()").extract_first(),
                'Kilometrage': response.xpath("//span[@itemprop='mileageFromOdometer']/text()").extract_first(),
                'Price': Price_without_space,
                'Time':  str(datetime.now()),
        }
        doc_id = "%s-%s-%s"%(article['Model'],str(datetime.now()),"ballouchi")
        el_cnx.index(index='ballouchi',doc_type='product',id=doc_id,body=article)
        #with open('D:\data3.csv', 'a') as f:
            #w = csv.DictWriter(f, article.keys(),newline="")
            #w.writerow(article)
        yield article
        


    def parse_links(self, response):
        articles= response.xpath("//div[@class='center_block']/h3/a/@href").extract()
        for article in articles:
            yield scrapy.Request(url="https://www.ballouchi.com"+article, callback=self.parse)
        next_page = response.xpath("//li[@id='pagination_next']/a/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin("https://www.ballouchi.com"+next_page)
            yield scrapy.Request(next_page, callback=self.parse_links)