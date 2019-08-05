from recursion_util import *
import collections
import fileinput
import json
import sys

fields_string = sys.argv[1]
field_parts = fields_string.split('+')

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

out_rows = []
seen_keys = set()
for row in data_rows:
	key_parts = []
	failed = False
	for field_part in field_parts:
		key_part = RecursiveRead(row, field_part)
		if not key_part:
			failed = True
		key_parts.append(key_part)
	if failed:
		continue
	key = '+'.join(key_parts)
	if key in seen_keys:
		pass
	else:
		seen_keys.add(key)
		out_rows.append(row)

print(json.dumps(out_rows, indent=2))
