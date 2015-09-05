# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class ComparatorItem(Item):
	"""Item object container for vividseats.com data"""
	eventname = Field()
	ticketprice = Field()
	eventlocation = Field()
	ticketslink = Field()
	eventdate = Field()
	eventcity = Field()
	eventstate = Field()
	eventtime = Field()