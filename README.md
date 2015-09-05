### Abstract
The files in this repo comprise a small app that scrapes two ticket sales websites for information and pricing about a
specific event and graphs the prices scraped from both sites. *Note: This is not a fully implemented app. This side-project was 
intended as a way to learn about implementing webscrapers and doing some data visualization on the scraped data.*

##Features
* **The web scrapers are written in the [Scrapy framework 1.0](https://github.com/scrapy/scrapy) 
    (more info info in the [scrapy docs](http://doc.scrapy.org/))**
* **Scrapy web spiders parse JSON data to retrieve prices from the websites**
* **Postgresql used as the DBMS**
* **Uses [Matplotlib](https://github.com/matplotlib/matplotlib) and [numpy](https://github.com/numpy/numpy) to plot the 
  changes in the lowest price for a concert in a particular place over time**
* **Scrapes concert tour data from vividseats.com and ticketcity.com**
* **Uses a bash script to run all of the files**

##Example use case
1. Open terminal
2. Run bash script:
    ``` $ ./scrapy_script.sh```
  * (3. Currently requires the user input of the name of a band/artist when the scrapy spider script runs but can be done 
    asynchronously using the [expect program](http://manpages.ubuntu.com/manpages/utopic/man1/expect.1.html) in the terminal)
    Upon the prompt of ```enter a bandname``` the user can enter a band or artist name  e.g. ```alt-j```
    
  * Graph is plotted:
    ![alt tag](https://cloud.githubusercontent.com/assets/8988459/9701364/1a67330e-53f3-11e5-9724-0103af7be503.png)
    
**Additional Feature**
  The bash script can be run asychronously using a crontab
  e.g. ```crontab -e```  
   ``` 0 12 * * * sh ~/Desktop/scrapers_repo/scrapy_script.py```
  
