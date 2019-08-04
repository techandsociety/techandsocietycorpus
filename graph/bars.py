import matplotlib.pyplot as plt
import numpy as np
from ts_util import *
import sys
from collections import defaultdict
import random
import json

Order = FileOrders.OLDEST

x_label_field = sys.argv[1]
y_field = sys.argv[2]

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

x_labels = []
y_values = []
for row in data_rows:
	x_labels.append(row[x_label_field])
	y_values.append(row[y_field])

ind = np.arange(len(x_labels))
width = 0.5 
fig, ax = plt.subplots()
rects1 = ax.bar(ind, y_values, width)
ax.set_ylabel('y_title')
ax.set_title('title')
ax.set_xticks(ind)
ax.set_xticklabels(x_labels, rotation=90)
fig.tight_layout()
fname = os.path.join(settings.output_image_path(), 'bar.png')
print('fname', fname)
plt.savefig(fname)
