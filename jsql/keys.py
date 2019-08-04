import analysis
import collections
import fileinput
import json
import sys

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

out_rows = []
for row in data_rows:
	out_rows.append(row[0])

print(json.dumps(out_rows, indent=2))
