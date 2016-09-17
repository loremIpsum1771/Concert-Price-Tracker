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
from vividseats_scraper.items import ComparatorItem
from urlparse import urljoin

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

bandname = raw_input("Enter bandname\n")
vs_url = "http://www.vividseats.com/concerts/" + bandname + "-tickets.html"


class MySpider(CrawlSpider):
    handle_httpstatus_list = [416]
    name = 'comparator'
    allowed_domains = ["www.vividseats.com"]
    start_urls = [vs_url]
    tickets_list_xpath = './/*[@itemtype="http://schema.org/Event"]'

    def createLink(self, bandname):
        vs_url = "http://www.vividseats.com/concerts/" + bandname + "-tickets.html"
        self.start_urls = [vs_url]     

    def parse_json(self, response):
        loader = response.meta['loader']
        #gets entire json file
        jsonresponse = json.loads(response.body_as_unicode())
        #gets 'tickets' object
        ticket_info = jsonresponse.get('tickets')
        #gets the price inside each ticket
        price_list = [i.get('p') for i in ticket_info]
        #checks whether or not there is a price for each ticket
        if len(price_list) > 0:
            str_Price = str(price_list[0])
            ticketprice = unicode(str_Price, "utf-8")
            loader.add_value('ticketprice', ticketprice)
        else:
            ticketPrice = unicode("sold out", "utf-8")
            loader.add_value('ticketprice', ticketPrice)
        return loader.load_item()
    def parse_price(self, response):
        loader = response.meta['loader']
        ticketsLink = loader.get_output_value("ticketslink")
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
            loader.add_xpath('eventname' , './/*[@class="productionsEvent"]/text()')
            loader.add_xpath('eventlocation' , './/*[@class = "productionsVenue"]/span[@itemprop  = "name"]/text()')
            loader.add_xpath('ticketslink' , './/*/a[@class = "btn btn-primary"]/@href')
            loader.add_xpath('eventdate' , './/*[@class = "productionsDate"]/text()')
            loader.add_xpath('eventcity' , './/*[@class = "productionsVenue"]/span[@itemprop  = "address"]/span[@itemprop  = "addressLocality"]/text()')
            loader.add_xpath('eventstate' , './/*[@class = "productionsVenue"]/span[@itemprop  = "address"]/span[@itemprop  = "addressRegion"]/text()')
            loader.add_xpath('eventtime' , './/*[@class = "productionsTime"]/text()')

            print "Here is ticket link \n" + loader.get_output_value("ticketslink")
            ticketsURL = "concerts/" + bandname + "-tickets/" + bandname + "-" + loader.get_output_value("ticketslink")
            ticketsURL = urljoin(response.url, ticketsURL)
            yield scrapy.Request(ticketsURL, meta={'loader': loader}, callback = self.parse_price, dont_filter = True)



def spiderCrawl(bandname):
   createLink(bandname)
   settings = get_project_settings()
   settings.set('USER_AGENT','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
   process = CrawlerProcess(settings)
   process.crawl(MySpider)
   process.start()
    
