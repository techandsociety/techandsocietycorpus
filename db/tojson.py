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
import sys
import ts_util
from collections import defaultdict
import csv
import datetime
import json
import os
import settings
import sys

query_filter = sys.argv[1]

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

rows = []
for r in session.query(Recommendation).filter(Recommendation.query == query_filter):
	rows.append({
		'date' : r.date,
		'idx' : r.scrape_idx,
		'publication' : r.publication,
		'title' : r.title,
		'google_url' : r.google_url,
		'query' : r.query,
	})
print (json.dumps(rows, indent=2))
session.close()
engine.dispose()
