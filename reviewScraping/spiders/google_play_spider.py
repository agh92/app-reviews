import scrapy


class GooglePlaySpider(scrapy.Spider):

    name = "googlePlay"

    def start_requests(self):
        urls = [
            'https://play.google.com/store/apps/details?id=de.volkswagen.carnet.eu.eremote&showAllReviews=true'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #textresponse
        print (response)
