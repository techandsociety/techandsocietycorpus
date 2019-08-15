from collections import defaultdict
from db.objects import Recommendation
import sqlalchemy
from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ts_util import *
import csv
import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import settings
import sqlalchemy
import sys

query_terms = [
	'donald trump',
]

Order = FileOrders.OLDEST

for query_term in query_terms:
	query_parts = query_term.split(' ')
	escaped_query_term = '%20'.join(query_parts)
	matches = GetFilesMatching(
		['type=news.query=' + escaped_query_term + '.', ':00:'],
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
		date_part = fname.split('date=')[-1]
		date_string = date_part.split('.')[0]
		datetime = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
		for jdx in range(len(result.sites)):
			r = Recommendation()
			r.time_scraped = datetime
			r.google_url = result.urls[jdx]
			r.publication = result.sites[jdx]
			r.query = query_term
			r.scrape_idx = jdx
			r.title = result.titles[jdx]
			# Check if this exists.
			existing = session.query(Recommendation).filter(
				Recommendation.time_scraped==r.time_scraped,
				Recommendation.google_url==r.google_url,
				Recommendation.publication==r.publication,
				Recommendation.query==r.query,
				Recommendation.scrape_idx==r.scrape_idx,
				Recommendation.title==r.title,
				).first()
			if not existing:
				session.add(r)
		break

session.commit()
session.close()
engine.dispose()
