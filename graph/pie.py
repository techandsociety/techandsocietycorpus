import settings
import os
from recursion_util import *
import collections
import fileinput
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import ts_util

field = sys.argv[1]
legend_file = sys.argv[2]

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

legend = {}
with open(legend_file, 'r') as f:
	pairs = [l.strip().split('\t') for l in f.readlines()]
	for pair in pairs:
		if len(pair) == 2:
			legend[pair[0]] = pair[1]
print(legend)

counts = collections.defaultdict(int)
for row in data_rows:
	value = RecursiveRead(row, field)
	assert value, value
	counts[value] += 1

labels = []
values = []
s = ts_util.GetSortedMapPairs(counts)
print(len(s))
for k, v in s:
	print(k, v)
	if k in legend:
		labels.append(legend[k])
	else:
		labels.append(k)
	values.append(v)

plt.pie(values, autopct='%1.1f%%', shadow=True,)
plt.legend(labels=labels, loc="best")
plt.axis('equal')
plt.tight_layout()
fname = os.path.join(settings.output_image_path(), 'pie_chart.png')
print(fname)
plt.savefig(fname)
