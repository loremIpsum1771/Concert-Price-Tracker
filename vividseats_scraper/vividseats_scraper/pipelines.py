from sqlalchemy.orm import sessionmaker
from models import Tickets, db_connect, create_vs_tickets_table





class ComparatorPipeline(object):
    """Price comparison pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_vs_tickets_table(engine)
        self.Session = sessionmaker(bind=engine)
    def process_item(self, item, spider):
        """Save tickets in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        ticket = Tickets(**item)

        try:
            session.add(ticket)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
