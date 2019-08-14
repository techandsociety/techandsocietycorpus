from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.types

Base = declarative_base()
class Recommendation(Base):
	__tablename__ = 'recommendation'
	id = Column(Integer, primary_key=True)
	date = Column(sqlalchemy.types.String(256))
	google_url = Column(sqlalchemy.types.String(2048))
	publication = Column(sqlalchemy.types.String(256))
	query = Column(sqlalchemy.types.String(256))
	scrape_idx = Column(Integer)
	title = Column(sqlalchemy.types.String(1024))

url = 'postgresql://tech:tech@127.0.0.1/techwatch'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Recommendation.metadata.drop_all(engine)
Recommendation.metadata.create_all(engine)

session.close()
engine.dispose()
