import collections
import csv
import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import settings
import sys

def ReadTuples(label_fname):
	try:
		label_rows = []
		with open(label_fname) as json_file:
			label_rows = json.load(json_file)
	except ValueError:
		pass
	counts = collections.defaultdict(int)
	print(len(label_rows))
	for row in label_rows:
		print(row)
		if not row['query'] == 'donald trump':
			continue
		if not 'rating' in row:
			continue
		print ('ok')
		counts[row['rating']] += 1
	def SortByValue(s):
		return -1 * s[1]
	s = sorted(list(counts.items()), key = SortByValue)
	labels = []
	means = []
	print(len(s))
	blacklist = {'n'}
	for k, v in s:
		if k in blacklist:
			continue
		print(k, v)
		labels.append(k)
		means.append(v)
	ind = np.arange(len(labels))  # the x locations for the groups
	width = 0.35  # the width of the bars
	if False:
		fig, ax = plt.subplots()
		rects1 = ax.bar(ind , means, width, label=None)
		ax.set_ylabel('y title')
		ax.set_title('title')
		ax.set_xticks(ind)
		ax.set_xticklabels(labels, rotation=90)
		fig.tight_layout()
	plt.pie(means, autopct='%1.1f%%', shadow=True,)
	plt.legend(labels=labels, loc="best")
	plt.axis('equal')
	plt.tight_layout()
	fname = os.path.join(settings.output_image_path(), 'pie_chart.png')
	print(fname)
	plt.savefig(fname)

if __name__ == "__main__":
	ReadTuples(sys.argv[1])
