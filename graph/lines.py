import matplotlib.dates as mdates
from sqlalchemy import func
import datetime
from collections import defaultdict
from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import sqlalchemy
import sys
from db.objects import Recommendation
import settings

url = 'postgresql://tech:tech@127.0.0.1/techwatch'
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

results = session.\
	query(Recommendation).\
	filter(Recommendation.query == 'donald trump')

count = 0
date_stories = defaultdict(list)
date_total = defaultdict(int)
for result in results.all():
	date_stories[result.time_scraped].append(result)
	date_total[result.time_scraped] += 1
session.close()
engine.dispose()

print('count', len(date_stories))

sorted_dates = sorted(date_total)
site_percents = defaultdict(list)
site_dates = defaultdict(list)
for date in sorted_dates:
	local_site_percents = defaultdict(float)
	divisor = date_total[date]
	for story in date_stories[date]:
		local_site_percents[story.publication] += 100.0 / divisor
	for k, v in local_site_percents.items():
		site_percents[k].append(v)
		site_dates[k].append(date)

site_mean = {}
site_std = {}
for k, percents in site_percents.items():
	site_mean[k] = np.mean(percents)
	site_std[k] = np.std(percents)

def SortByValue(s):
	return -1 * s[1]
site_mean_sorted = sorted(site_mean.items(), key = SortByValue)
print(site_mean_sorted)

# Make the line graph.
legend = []
fig, ax = plt.subplots() # figsize=(15,15))
plt.ylabel('Percent of articles', fontsize=12)
plt.xlabel('Time', fontsize=12)
plt.title('Percent publication use over time for "Donald Trump"')
for k, kv in site_mean_sorted[:10]:
	print(k, site_dates[k])
	print(k, site_percents[k])
	plt.plot(site_dates[k], site_percents[k])
	legend.append(k)
plt.legend(legend, loc='upper left')
ax.set_xticklabels(sorted_dates, rotation=90)
fname = os.path.join(settings.output_image_path(), 'lines.png')
myFmt = mdates.DateFormatter('%m/%d')
ax.xaxis.set_major_formatter(myFmt)
print(fname)
plt.savefig(fname)

