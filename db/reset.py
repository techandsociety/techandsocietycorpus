from db.objects import Recommendation
from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import sqlalchemy.types

url = 'postgresql://tech:tech@127.0.0.1/techwatch'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Recommendation.metadata.drop_all(engine)
Recommendation.metadata.create_all(engine)

session.close()
engine.dispose()
