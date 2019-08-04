import matplotlib.pyplot as plt
import numpy as np
import ts_util
from collections import defaultdict
import csv
import datetime
import json
import os
import settings
import sys

DoCheck = False
def GetUrl(row): return row['google_url']
def GetTitle(row): return row['title']
query_count = defaultdict(int)
query_positive = defaultdict(int)
querysite_count = defaultdict(int)
querysite_positive = defaultdict(int)
def GetMatchingRows(in_fname, word_list):
	all_rows = []
	with open(in_fname) as json_file:
		all_rows = json.load(json_file)
	unique_rows = []
	seen_urls = set()
	num_pruned_rows = 0
	for row in all_rows:
		url = GetUrl(row)
		if url in seen_urls:
			num_pruned_rows += 1
		else:
			unique_rows.append(row)
			seen_urls.add(url)
	if DoCheck:
		# check rows
		seen_check = set()
		for row in unique_rows:
			url = GetUrl(row)
			if url in seen_check:
				sys.exit(1)
			seen_check.add(url)
	matching_rows = []
	for row in unique_rows:
		found = False
		title = GetTitle(row).lower()
		for word in word_list:
			tokenized_title = title.split(' ')
			if word in tokenized_title:
				found = True
		query_count[row['query']] += 1
		querysite_count[(row['query'], row['publication'])] += 1
		if found:
			query_positive[row['query']] += 1
			querysite_positive[(row['query'], row['publication'])] += 1
			matching_rows.append(row)
	return matching_rows, all_rows
if __name__ == "__main__":
	studies = []
	studies.append(['race', 'racial', 'racist', 'racism', 'races'])
	studies.append(['mueller', 'russia'])
	fig, ax = plt.subplots()
	for study in studies:
		matching_files = ts_util.GetFilesMatching(['trump',':00:'], settings.git_data_path(), ts_util.FileOrders.OLDEST)
		seen_urls = set()
		matching_rows = []
		dates = []
		row_percents = []
		for match in matching_files:
			rows, all_rows = GetMatchingRows(match, study)
			if not rows:
				print('not rows')
				continue
			date_string = rows[0]['date'].split('.')[0]
			date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
			dates.append(date)
			row_percents.append(len(rows) * 100.0 / len(all_rows))
			for row in rows:
				url = GetUrl(row)
				if url in seen_urls:
					pass
				else:
					seen_urls.add(url)
					matching_rows.append(row)
		plt.plot(dates, row_percents, label=study)
	plt.legend(loc='upper left')
	ax.set_ylabel('y_title')
	ax.set_title('title')
	ax.xaxis_date()
	plt.xticks(rotation=90)
	fig.tight_layout()
	fname = os.path.join(settings.output_image_path(), 'matches.png')
	print('fname', fname)
	print(row_percents)
	plt.savefig(fname)
