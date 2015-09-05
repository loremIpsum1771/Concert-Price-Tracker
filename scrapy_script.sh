#!/usr/bin/expect


cd ~/Desktop/scrapers_repo
python clear_db.py
cd ~/Desktop/scrapers_repo/vividseats_scraper
scrapy crawl comparator
# spawn scrapy crawl comparator
# expect "Enter a bandname \n"
# send "alt-j"
cd ~/Desktop/scrapers_repo/ticket_city_scraper
scrapy crawl comparator
# spawn scrapy crawl comparator
# expect "Enter a bandname \n"
# send "alt-j"
cd ~/Desktop/scrapers_repo
python priceGrapher.py

