import collections
import csv
import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import settings
import sys

StopWord = 'stop'
def ReadTuples(label_fname):
	try:
		label_rows = []
		with open(label_fname) as json_file:
			label_rows = json.load(json_file)
	except ValueError:
		pass
	yes_counts = collections.defaultdict(int)
	no_counts = collections.defaultdict(int)
	blacklist = {'n'}
	for row in label_rows:
		if not 'rating' in row:
			continue
		if row['query'] != 'donald trump':
			continue
		if row['rating'] in blacklist:
			continue
		if row['rating'] == 't' or row['rating'] == 'ct':
			yes_counts[row['publication']] += 1
		else:
			print(row)
			no_counts[row['publication']] += 1
	def SortByValue(s):
		return -1 * s[1]
	s = sorted(list(yes_counts.items()), key = SortByValue)
	labels = []
	yes_means = []
	no_means = []
	for k, v in s:
		if k in blacklist:
			continue
		labels.append(k)
		yes_means.append(v)
		no_means.append(no_counts[k])
	ind = np.arange(len(labels))  # the x locations for the groups
	width = 0.35  # the width of the bars
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind , yes_means, width, label=None)
	# rects2 = ax.bar(ind , no_means, width, bottom = yes_means, label=None)
	ax.set_ylabel('y title')
	ax.set_title('title')
	ax.set_xticks(ind)
	ax.set_xticklabels(labels, rotation=90)
	fig.tight_layout()
	fname = os.path.join(settings.output_image_path(), 'matches.png')
	print(fname)
	plt.savefig(fname)

if __name__ == "__main__":
	ReadTuples(sys.argv[1])
