from recursion_util import *
import collections
import fileinput
import json
import sys

field = sys.argv[1]
op = sys.argv[2]
value = sys.argv[3]

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

out_rows = []
for row in data_rows:
	if op == 'eq':
		if RecursiveRead(row, field) == value:
			out_rows.append(row)
	elif op == 'neq':
		if RecursiveRead(row, field) != value:
			out_rows.append(row)
	else:
		assert False, op

print(json.dumps(out_rows, indent=2))
