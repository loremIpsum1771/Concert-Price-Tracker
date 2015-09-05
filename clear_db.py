import psycopg2

conn = psycopg2.connect(database = "scrape")
#prepare a cursor
cur = conn.cursor()

vs_query = """ delete from vs_tickets """

cur.execute(vs_query)
conn.commit()

tc_query = """ delete from tc_tickets """

cur.execute(tc_query)
conn.commit()

cur.close()
conn.close()


