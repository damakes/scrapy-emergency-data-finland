import scrapy
from emerscraper.items import EmerItem

class EmerspiderSpider(scrapy.Spider):
    name = "emerspider"
    allowed_domains = ["hälytyslista.fi"]
    start_urls = ["https://hälytyslista.fi/"]


    custom_settings = {
        'FEEDS' : {
            'emersnow.csv':{'format':'csv','overwrite': False},
            }
    }

    def parse(self, response):
        emer_item = EmerItem()
        for emer in response.css('li.wrapper'):
            emer_item['location'] = emer.css('div.gtc::text').get(),
            emer_item['type'] = emer.css('div.gtt::text').get(),
            emer_item['date'] = emer.css('div.gdd::attr(aria-label)').get().split(' ')[0],
            emer_item['time'] = emer.css('div.gdd::attr(aria-label)').get().split(' ')[1],

            yield emer_item
