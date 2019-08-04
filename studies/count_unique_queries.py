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
def GetMatchingRows(in_fname):
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
	return unique_rows
	return matching_rows
if __name__ == "__main__":
	queries_of_interest = [
		"donald trump",
#		"joe biden",
#		"kamala harris",
#		"elizabeth warren",
#		"hillary clinton",
#		"ilhan omar",
#		"andrew yang",
#		"alex jones",
#		"bernie sanders",
	]
	matching_files = analysis.GetFilesMatching(['trump', ':00:'], settings.git_data_path(), analysis.FileOrders.OLDEST)
	seen_urls = set()
	total_rows = 0
	for match in matching_files:
		rows = GetMatchingRows(match)
		for row in rows:
			url = GetUrl(row)
			if url in seen_urls:
				pass
			else:
				seen_urls.add(url)
				total_rows += 1
	print(total_rows)
