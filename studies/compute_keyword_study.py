import matplotlib.pyplot as plt
import numpy as np
import sys
import ts_util
from collections import defaultdict
import csv
import datetime
import json
import os
import settings
import sys

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
	return matching_rows
if __name__ == "__main__":
	if sys.argv[2] == 'racism':
		word_list = ['race', 'racial', 'racist', 'racism', 'races']
	elif sys.argv[2] == 'mueller':
		word_list = ['mueller', 'russia']
	elif sys.argv[2] == 'black':
		word_list = ['black', 'african']
	else:
		print('no study name found')
		sys.exit(1)
	query_filter = sys.argv[3]
	matching_files = ts_util.GetFilesMatching([query_filter,':00:'], settings.git_data_path(), ts_util.FileOrders.OLDEST)
	seen_urls = set()
	matching_rows = []
	dates = []
	row_counts = []
	novel_counts = []
	for idx, match in enumerate(matching_files):
		rows = GetMatchingRows(match, word_list)
		if not rows:
			print('not rows')
			continue
		novel_rows = 0
		for row in rows:
			url = GetUrl(row)
			if url in seen_urls:
				pass
			else:
				seen_urls.add(url)
				matching_rows.append(row)
				novel_rows += 1
		if idx > 0:
			row_counts.append(len(rows))
			novel_counts.append(novel_rows)
			date_string = rows[0]['date'].split('.')[0]
			date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
			dates.append(date)
	output_name = sys.argv[1]
	with open(output_name, "w") as write_file:
		json.dump(matching_rows, write_file, indent = 2)
	#Make graph
	ind = np.arange(len(row_counts))
	width = 1.0 
	fig, ax = plt.subplots()
	labels = []
	for idx, l in enumerate(row_counts):
		if idx % 10 == 0:
			labels.append(str(idx))
		else:
			labels.append('')
	ax.set_ylabel('y_title')
	plt.plot(dates, row_counts)
	plt.plot(dates, novel_counts)
	ax.set_title('title')
	ax.xaxis_date()
	plt.xticks(rotation=90)
	print(dates)
	fig.tight_layout()
	fname = os.path.join(settings.output_image_path(), 'matches.png')
	print('fname', fname)
	print(row_counts)
	plt.savefig(fname)
