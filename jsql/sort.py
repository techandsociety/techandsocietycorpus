import analysis
import collections
import fileinput
import json
import sys


lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)
sort_field = sys.argv[1]

pub_rows = collections.defaultdict(list)
for row in data_rows:
	pub_rows[row[sort_field]].append(row)

s = sorted(list(pub_rows.items()), key=analysis.SortByValueLen)
print(json.dumps(s, indent=2))
