import collections
import json
import sys
import ts_util

field = sys.argv[1]

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

field_rows = collections.defaultdict(list)
for row in data_rows:
	value = row[field]
	field_rows[value].append(row)

s = sorted(list(field_rows.items()), key = ts_util.SortByKey)
rows = []
for k, v in s:
	rows.append([k, v])

print(json.dumps(rows, indent=2))
