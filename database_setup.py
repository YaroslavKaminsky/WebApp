from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import config
from sqlalchemy import create_engine


Base = declarative_base()

class Currency_table(Base):
   __tablename__ = 'usd_currency'

   id = Column(Integer, primary_key=True)
   name = Column(String(3))
   value = Column(Integer)
   time_stamp = Column(String(25))


#creates a create_engine instance at the bottom of the file
print(config.DATABASE_URL)
engine = create_engine(config.DATABASE_URL)
print('created')

Base.metadata.create_all(engine)
