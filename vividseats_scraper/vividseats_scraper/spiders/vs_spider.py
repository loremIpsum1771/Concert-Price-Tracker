import scrapy
import re
import json
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider , Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scraper.items import ComparatorItem
from urlparse import urljoin

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging


class MySpider(CrawlSpider):
    handle_httpstatus_list = [416]
    name = 'comparator'
    allowed_domains = ["www.vividseats.com"]
    #start_urls = [vs_url]
    tickets_list_xpath = './/*[@itemtype="http://schema.org/Event"]'

    def createLink(self, bandname):
        vs_url = "http://www.vividseats.com/concerts/" + bandname + "-tickets.html"
        self.start_urls = [vs_url]     

    def parse_json(self, response):
        loader = response.meta['loader']
        jsonresponse = json.loads(response.body_as_unicode())
        ticket_info = jsonresponse.get('tickets')
        price_list = [i.get('p') for i in ticket_info]
        if len(price_list) > 0:
            str_Price = str(price_list[0])
            ticketPrice = unicode(str_Price, "utf-8")
            loader.add_value('ticketPrice', ticketPrice)
        else:
            ticketPrice = unicode("sold out", "utf-8")
            loader.add_value('ticketPrice', ticketPrice)
        return loader.load_item()
    def parse_price(self, response):
        loader = response.meta['loader']
        ticketsLink = loader.get_output_value("ticketsLink")
        json_id_list= re.findall(r"(\d+)[^-]*$", ticketsLink)
        json_id=  "".join(json_id_list)
        json_url = "http://www.vividseats.com/javascript/tickets.shtml?productionId=" + json_id
        yield scrapy.Request(json_url, meta={'loader': loader}, callback = self.parse_json, dont_filter = True) 

    def parse(self, response):
        """
        # """
        selector = HtmlXPathSelector(response)
        # iterate over tickets
        for ticket in selector.select(self.tickets_list_xpath):
            loader = XPathItemLoader(ComparatorItem(), selector=ticket)
            # define loader
            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()
            # iterate over fields and add xpaths to the loader
            loader.add_xpath('eventName' , './/*[@class="productionsEvent"]/text()')
            loader.add_xpath('eventLocation' , './/*[@class = "productionsVenue"]/span[@itemprop  = "name"]/text()')
            loader.add_xpath('ticketsLink' , './/*/a[@class = "btn btn-primary"]/@href')
            loader.add_xpath('eventDate' , './/*[@class = "productionsDate"]/text()')
            loader.add_xpath('eventCity' , './/*[@class = "productionsVenue"]/span[@itemprop  = "address"]/span[@itemprop  = "addressLocality"]/text()')
            loader.add_xpath('eventState' , './/*[@class = "productionsVenue"]/span[@itemprop  = "address"]/span[@itemprop  = "addressRegion"]/text()')
            loader.add_xpath('eventTime' , './/*[@class = "productionsTime"]/text()')

            print "Here is ticket link \n" + loader.get_output_value("ticketsLink")
            #sel.xpath("//span[@id='PractitionerDetails1_Label4']/text()").extract()
            ticketsURL = "concerts/" + bandname + "-tickets/" + bandname + "-" + loader.get_output_value("ticketsLink")
            ticketsURL = urljoin(response.url, ticketsURL)
            yield scrapy.Request(ticketsURL, meta={'loader': loader}, callback = self.parse_price, dont_filter = True)



def spiderCrawl(bandname):
   createLink(bandname)
   settings = get_project_settings()
   settings.set('USER_AGENT','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
   process = CrawlerProcess(settings)
   process.crawl(MySpider)
   process.start()
    
#     configure_logging()
# runner = CrawlerRunner()

# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(MySpider)
#     yield runner.crawl(MySpider3)
#     reactor.stop()

# crawl()
# reactor.run()
