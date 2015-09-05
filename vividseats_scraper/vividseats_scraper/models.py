from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime
import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_vs_tickets_table(engine):
	DeclarativeBase.metadata.create_all(engine)
    
class Tickets(DeclarativeBase):
    """Sqlalchemy tickets model"""
    __tablename__ = "vs_tickets"

    id = Column(Integer, primary_key=True)
    eventname = Column('eventname', String)
    ticketprice = Column('ticketprice', String, nullable=True)
    eventlocation = Column('eventlocation', String, nullable=True)
    ticketslink = Column('ticketslink', String, nullable=True)
    eventdate = Column('eventdate', String, nullable=True)
    eventcity = Column('eventcity', String, nullable=True)
    eventstate = Column('eventstate', String, nullable=True)
    eventtime = Column('eventtime', String, nullable=True)
    
