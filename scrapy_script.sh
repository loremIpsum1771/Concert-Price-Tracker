#!/bin/bash
# My first script

#echo "Hello World!"
cd ~/Desktop/scrapers_repo
python clear_db.py
cd ~/Desktop/scrapers_repo/vividseats_scraper
scrapy crawl comparator
cd ~/Desktop/scrapers_repo/ticket_city_scraper
scrapy crawl comparator
cd ~/Desktop/scrapers_repo
python priceGrapher.py

#export PATH=$PATH:directory