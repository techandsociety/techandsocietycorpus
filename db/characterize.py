from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer
from ts_util import *
from sqlalchemy.ext.declarative import declarative_base
from collections import defaultdict
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import settings
import sys

Deref = False
Order = FileOrders.OLDEST
DontRegenerate = True

Base = declarative_base()
class Recommendation(Base):
	__tablename__ = 'recommendation'
	id = Column(Integer, primary_key=True)
	# page_views = Column(Integer)
	# date = Column(sqlalchemy.types.Date())
	user_id = Column(Integer)
	publication = Column(sqlalchemy.types.String(256))
	title = Column(sqlalchemy.types.String(1024))
	google_url = Column(sqlalchemy.types.String(2048))

url = 'postgresql://tech:tech@127.0.0.1/techwatch'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

count = 0
for r in session.query(Recommendation):
	count += 1
print(count)
session.close()
engine.dispose()
