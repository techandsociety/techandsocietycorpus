import json
import sys

lines = ''.join(sys.stdin.readlines())
data_rows = json.loads(lines)
print(len(data_rows))
