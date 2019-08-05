from recursion_util import *
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
	keyword = sys.argv[1]
	label_file = sys.argv[2]
	if label_file != '-':
		use_label_file = True
	else:
		use_label_file = False
	if use_label_file:
		rating_field = sys.argv[3]
	substantial_urls = set()
	if use_label_file:
		with open(label_file, 'r') as infile:
			rows = json.load(infile)
			for row in rows:
				rating = RecursiveRead(row, rating_field)
				if rating != 'n':
					substantial_urls.add(row['google_url'])
				else:
					print (row)
	if keyword == 'racism':
		word_list = ['race', 'racial', 'racist', 'racism', 'races']
	elif keyword == 'mueller':
		word_list = ['mueller', 'russia']
	else:
		print('no study name found')
		sys.exit(1)
	fig, ax = plt.subplots()
	for query_filter in queries:
		matching_files = ts_util.GetFilesMatching([query_filter,':00:'], settings.git_data_path(), ts_util.FileOrders.OLDEST)
		seen_urls = set()
		matching_rows = []
		dates = []
		row_percents = []
		for match in matching_files:
			rows, all_rows = GetMatchingRows(match, word_list)
			if not rows:
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
					if not use_label_file or url in substantial_urls:
						seen_urls.add(url)
						matching_rows.append(row)
					else:
						pass
		plt.plot(dates, row_percents, label=query_filter.replace('%20', ' '))
	plt.legend(loc='upper left')
	ax.set_ylabel('Percent')
	ax.set_title('Percent of articles using a "race" word')
	ax.xaxis_date()
	plt.xticks(rotation=90)
	fig.tight_layout()
	fname = os.path.join(settings.output_image_path(), 'matches.png')
	print('fname', fname)
	print(row_percents)
	plt.savefig(fname)
