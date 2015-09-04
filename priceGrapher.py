#module to access PostgreSQL databases
import psycopg2
# matplotlib pyplot module
import matplotlib.pyplot as plt
import psycopg2
import time
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np


conn = psycopg2.connect(database = "scrape")
#prepare a cursor
cur = conn.cursor()

#query1 """ insert into lowestPrices values()"""

query2 = """
select ticketprice, eventdate from vs_tickets where eventstate = 'CA' order by ticketprice limit 1
"""
#execute the query
cur.execute(query2)

#retrieve the whole result set 
data = cur.fetchall()

#unpack data in price and date

vs_price, vs_eventDate = zip(*data)


query3 = """ insert into lowestPrices (price) values( %s) """
data = (vs_price)

cur.execute(query3, data)
conn.commit()


query4 = """ select scrape_dt,price from lowestPrices """
coordinateList  = []
dateList = []
cur.execute(query4)
rows= cur.fetchall()
for row in rows:
	pair = (row[0], row[1])
	coordinateList.append(pair)
fig, ax = plt.subplots()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'+ '/' '%d' + '/' '%Y'))
plt.gca().yaxis.set_major_locator(mdates.DayLocator())



ax.set_ylim([30,60])

xs = [x[0] for x in rows]
ys = [y[1] for y in rows]
idx = np.argsort(xs)
xs = np.array(xs)[idx]
ys = np.array(ys)[idx]
plt.plot(xs,ys, 'r-o')

# get data from tc_scraper 

tc_query = """select ticketprice, eventdate from tc_tickets where eventstate = 'CA' order by ticketprice limit 1"""

cur.execute(tc_query)

data = cur.fetchall()

tc_price, tc_eventDate = zip(*data)

#insert into lowestPrices table
query3 = """ insert into tc_lowestPrices (price) values( %s) """
data = (tc_price)

cur.execute(query3, data)
conn.commit()


tc_query2 = """ select scrape_dt,price from tc_lowestPrices """
cur.execute(tc_query2)
tc_rows= cur.fetchall()
for row in tc_rows:
	pair = (row[0], row[1])
	coordinateList.append(pair)

# Actually plot the data
tc_xs = [x[0] for x in tc_rows]
tc_ys = [y[1] for y in tc_rows]
tc_idx = np.argsort(tc_xs)
tc_xs = np.array(tc_xs)[tc_idx]
tc_ys = np.array(tc_ys)[tc_idx]
plt.plot(tc_xs,tc_ys, 'b-o')


# Fix ticklabels so they don't overlap in the figure
plt.gcf().autofmt_xdate()


# graph.plot(xs,ys, 'r-o')

#graph.set_xticks(xs)


#plt.plot(xs, ys)
plt.title("Cheapest Alt-J California concert tickets over time")
plt.xlabel("Date")
plt.ylabel("Ticket Price")	
plt.show()

#print len(priceList)
print len(dateList)
cur.close()
conn.close()
