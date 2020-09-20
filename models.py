from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import datetime

from config import db

DeclarativeBase = declarative_base()

db_url = "mysql+pymysql://%s:%s@%s/%s?charset=UTF8MB4" % (db.get('username'), db.get('password'), db.get('host'), db.get('db'))

def db_connect():
    '''Create connection to database'''
    return create_engine(db_url, encoding='utf-8', poolclass=NullPool)

def create_db_session(engine):
    '''Create session with database'''
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    return session

Base = declarative_base()
metadata = Base.metadata

class powerData(Base):
    '''
    App for power statistics from my house
    '''
    __tablename__ = 'powerConsumptionData'
    created = Column(DateTime, server_default=func.now())
    start = Column(DateTime, nullable=False, primary_key=True)
    end = Column(DateTime, nullable=False, primary_key=True)
    KwH = Column(Float, nullable=False)

if __name__ == "__main__":
    print('Creating connection')
    engine = db_connect()
    session = create_db_session(engine)
    print('Dropping table')
    powerData.__table__.drop(engine)
    print('Done dropping table')
    Base.metadata.create_all(engine)
    print('Done creating table')