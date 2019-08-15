from sqlalchemy import func
import datetime
from collections import defaultdict
from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ts_util import *
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import settings
import sqlalchemy
import sys
from db.objects import Recommendation

test_name = sys.argv[1]

def RunTest(name):
	return name == test_name

url = 'postgresql://tech:tech@127.0.0.1/techwatch'
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

if RunTest('select all'):
	count = session.query(Recommendation).count()
	print('count', count)

if RunTest('filter by time'):
	date_string = '2019-08-11T00:00:01'
	reference_time = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
	count = session.query(Recommendation).filter(Recommendation.time_scraped >= reference_time).count()
	print('count', count)

if RunTest('select field'):
	results = session.query(Recommendation.publication)
	for result in results:
		print(result.publication)

if RunTest('select unique field'):
	results = session.query(Recommendation.publication).distinct()
	for result in results:
		print(result.publication)

if RunTest('count *'):
	count1 = session.query(Recommendation).count()
	print('count1', count1)
	count2 = session.query(func.count('*')).select_from(Recommendation).scalar()
	print('count2', count2)

if RunTest('order by count'):
	results = session.query(func.count(Recommendation.publication), Recommendation.publication).group_by(Recommendation.publication).order_by(sqlalchemy.text('count_1')).all()
	results = list(reversed(list(results)))
	print(results)

"""
select 
"""
if True or RunTest('order by count'):
	results = session.\
		query(func.count(), func.sum(func.count()), Recommendation.publication, Recommendation.time_scraped)
	results = results.\
		group_by(Recommendation.time_scraped, Recommendation.publication).\
		order_by(sqlalchemy.text('count_1'))
	print (results)
	for result in results.all():
		print result

session.close()
engine.dispose()
