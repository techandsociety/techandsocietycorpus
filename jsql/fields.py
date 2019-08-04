from recursion_util import *
import collections
import fileinput
import json
import sys

operation = sys.argv[1]
def IsCopy():
	return operation in ['move', 'copy']
def IsDelete():
	return operation in ['move', 'delete']

src_field = sys.argv[2]

if IsCopy():
	dest_field = sys.argv[3]

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)

out_rows = []
for row in data_rows:
	if IsCopy():
		curr_value = RecursiveRead(row, src_field)
		if not curr_value:
			continue
		RecursiveSet(row, dest_field, curr_value)
	if IsDelete():
		RecursiveDelete(row, src_field)
	out_rows.append(row)

print(json.dumps(out_rows, indent=2))
