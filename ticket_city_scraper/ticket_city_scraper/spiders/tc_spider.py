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
from ticket_city_scraper.items import ComparatorItem
from urlparse import urljoin

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging



bandname = raw_input("Enter a bandname \n")
tc_url = "https://www.ticketcity.com/concerts/" + bandname + "-tickets.html"

class MySpider3(CrawlSpider):
    handle_httpstatus_list = [416]
    name = 'comparator'
    allowed_domains = ["www.ticketcity.com"]
    start_urls = [tc_url]
    tickets_list_xpath = './/div[@class = "vevent"]'
    
    def parse_json(self, response):
        loader = response.meta['loader']
        jsonresponse = json.loads(response.body_as_unicode())
        ticket_info = jsonresponse.get('B')
        price_list = [i.get('P') for i in ticket_info]
        if len(price_list) > 0:
            str_Price = str(price_list[0])
            ticketprice = unicode(str_Price, "utf-8")
            loader.add_value('ticketprice', ticketprice)
        else:
            ticketPrice = unicode("sold out", "utf-8")
            loader.add_value('ticketprice', ticketprice)
        return loader.load_item()

    def parse_price(self, response):
        print "parse price function entered \n"
        loader = response.meta['loader']
        event_city = response.xpath('.//span[@itemprop="addressLocality"]/text()').extract() 
        eventcity = ''.join(event_city) 
        loader.add_value('eventcity' , eventcity)
        event_state = response.xpath('.//span[@itemprop="addressRegion"]/text()').extract() 
        eventstate = ''.join(event_state) 
        loader.add_value('eventstate' , eventstate) 
        event_date = response.xpath('.//span[@class="event_datetime"]/text()').extract() 
        eventdate = ''.join(event_date)  
        loader.add_value('eventdate' , eventdate)    
        ticketslink = loader.get_output_value("ticketslink")
        json_id_list= re.findall(r"(\d+)[^-]*$", ticketslink)
        json_id=  "".join(json_id_list)
        json_url = "https://www.ticketcity.com/Catalog/public/v1/events/" + json_id + "/ticketblocks?P=0,99999999&q=0&per_page=250&page=1&sort=p.asc&f.t=s&_=1436642392938"
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
            loader.add_xpath('eventname' , './/span[@class="summary listingEventName"]/text()')
            loader.add_xpath('eventlocation' , './/div[@class="divVenue location"]/text()')
            loader.add_xpath('ticketslink' , './/a[@class="divEventDetails url"]/@href')
            
            print "Here is ticket link \n" + loader.get_output_value("ticketslink")
            ticketsURL = "https://www.ticketcity.com/" + loader.get_output_value("ticketslink")
            ticketsURL = urljoin(response.url, ticketsURL)
            yield scrapy.Request(ticketsURL, meta={'loader': loader}, callback = self.parse_price, dont_filter = True)
