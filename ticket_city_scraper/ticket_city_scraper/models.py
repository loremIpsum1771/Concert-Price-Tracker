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


def create_tc_tickets_table(engine):

    DeclarativeBase.metadata.create_all(engine)

class Tickets(DeclarativeBase):
    """Sqlalchemy tickets3 model"""
    __tablename__ = "tc_tickets"

    id = Column(Integer, primary_key=True)
    eventName = Column('eventName', String)
    ticketPrice = Column('ticketPrice', String, nullable=True)
    eventLocation = Column('eventLocation', String, nullable=True)
    ticketsLink = Column('ticketsLink', String, nullable=True)
    eventDate = Column('eventDate', String, nullable=True)
    eventCity = Column('eventCity', String, nullable=True)
    eventState = Column('eventState', String, nullable=True)