import matplotlib.pyplot as plt
import numpy as np
import analysis
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
	queries = [
		"donald%20trump",
		"joe%20biden",
		"kamala%20harris",
		"elizabeth%20warren",
		"hillary%20clinton",
		"ilhan%20omar",
		"andrew%20yang",
		"bernie%20sanders",
	]
	if sys.argv[2] == 'racism':
		word_list = ['race', 'racial', 'racist', 'racism', 'races']
	elif sys.argv[2] == 'mueller':
		word_list = ['mueller', 'russia']
	elif sys.argv[2] == 'black':
		word_list = ['black', 'african']
	else:
		print('no study name found')
		sys.exit(1)
	fig, ax = plt.subplots()
	for query_filter in queries:
		matching_files = analysis.GetFilesMatching([query_filter,':00:'], settings.git_data_path(), analysis.FileOrders.OLDEST)
		seen_urls = set()
		matching_rows = []
		dates = []
		row_percents = []
		for match in matching_files:
			rows, all_rows = GetMatchingRows(match, word_list)
			if not rows:
				print('not rows')
				continue
			date_string = rows[0]['date'].split('.')[0]
			date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
			dates.append(date)
			row_percents.append(len(rows) * 1.0 / len(all_rows))
			for row in rows:
				url = GetUrl(row)
				if url in seen_urls:
					pass
				else:
					seen_urls.add(url)
					matching_rows.append(row)
		plt.plot(dates, row_percents, label=query_filter)
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
