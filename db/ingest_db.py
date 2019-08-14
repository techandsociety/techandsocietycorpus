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
	date = Column(sqlalchemy.types.String(256))
	google_url = Column(sqlalchemy.types.String(2048))
	publication = Column(sqlalchemy.types.String(256))
	query = Column(sqlalchemy.types.String(256))
	scrape_idx = Column(Integer)
	title = Column(sqlalchemy.types.String(1024))

matches = GetFilesMatching(
	[':00:'],
	settings.raw_data_path(),
	Order
	)
total_lines = 0

url = 'postgresql://tech:tech@127.0.0.1/techwatch'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

for idx, fname in enumerate(matches):
	print('doing', fname)
	result = GetAnalyzerResult(fname)
	json_result = []
	for jdx in range(len(result.sites)):
		google_url = result.urls[jdx]
		existing_or = session.query(Recommendation).filter(Recommendation.google_url==google_url).first()
		if existing_or:
			continue
		r = Recommendation()
		r.date = fname.split('date=')[-1]
		r.google_url = google_url
		r.publication = result.sites[jdx]
		r.query = 'TODO'
		r.scrape_idx = jdx
		r.title = result.titles[jdx]
		session.add(r)

session.commit()
session.close()
engine.dispose()
