import collections
import json
import sys
import ts_util

field = sys.argv[1]

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

out_pairs = []
for pair in data_rows:
	key = pair[0]
	value = pair[1]
	counts = collections.defaultdict(int)
	total = 0
	for row in value:
		counts[row[field]] += 1
		total += 1
	for k, v in counts.items():
		counts[k] = v * 100.0 / total
	out_pairs.append([key, counts])

print(json.dumps(out_pairs, indent=2))
