import settings
import os
import matplotlib.pyplot as plt
import numpy as np
from ts_util import *
import sys
from collections import defaultdict
import random
import json


lines = ''.join(sys.stdin.readlines())
print(lines)
data_rows = json.loads(lines)

outer_site_counts = defaultdict(list)
outer_site_x = defaultdict(list)
for idx, site_counts in data_rows:
	for k, v in site_counts.items():
		outer_site_counts[k].append(v)
		outer_site_x[k].append(idx)

outer_site_means = {}
outer_site_stds = {}
for k, v in outer_site_counts.items():
	outer_site_means[k] = np.mean(v)
	outer_site_stds[k] = np.std(v)

sorted_means = GetSortedMap(outer_site_means)
labels = []
means = []
stds = []
for k in sorted_means[:10]:
	labels.append(k)
	means.append(outer_site_means[k])
	stds.append(outer_site_stds[k])

ind = np.arange(len(labels))
width = 0.5 
fig, ax = plt.subplots()
print(means)
print(stds)
rects1 = ax.bar(ind, means, width, yerr = stds)
ax.set_ylabel('Percentage')
ax.set_title('Percent of Articles by Publication for "Donald Trump"')
ax.set_xticks(ind)
ax.set_xticklabels(labels, rotation=90)
fig.tight_layout()
fname = os.path.join(settings.output_image_path(), 'averages.png')
print('fname', fname)
plt.savefig(fname)
