import settings
import datetime
import matplotlib.pyplot as plt
import numpy as np
from ts_util import *
import sys
from collections import defaultdict
import os
import random
import json

Order = FileOrders.OLDEST

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

outer_site_counts = defaultdict(list)
outer_site_x = defaultdict(list)
labels = []
i = 0
for idx, site_counts in data_rows:
	date_string = idx.split('.')[0]
	date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
	labels.append('')
	total_sites = 0
	for k, v in site_counts.items():
		total_sites += v
	for k, v in site_counts.items():
		outer_site_counts[k].append(v)
		outer_site_x[k].append(date)
	i += 1

outer_site_averages = {}
for k, v in outer_site_counts.items():
	outer_site_averages[k] = np.mean(v)

sorted_averages = GetSortedMap(outer_site_averages)
legend = []
fig, ax = plt.subplots() # figsize=(15,15))

for k in sorted_averages[:10]:
	plt.plot(outer_site_x[k], outer_site_counts[k])
	legend.append(k)

plt.legend(legend, loc='upper left')
plt.ylabel('y', fontsize=12)
plt.xlabel('x', fontsize=12)
ax.set_xticklabels(labels, rotation=90)
fname = os.path.join(settings.output_image_path(), 'lines.png')
print(fname)
plt.savefig(fname)

