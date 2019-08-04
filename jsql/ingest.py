import sys
import ts_util
from collections import defaultdict
import csv
import datetime
import json
import os
import settings
import sys

query_filter = sys.argv[1]
data_path = settings.git_data_path()
matching_files = ts_util.GetFilesMatching([query_filter,':00:'], data_path, ts_util.FileOrders.OLDEST)

rows = []
for fn in matching_files:
	with open(fn, 'r') as infile:
		data_rows = json.load(infile)
	rows += data_rows
print (json.dumps(rows, indent=2))
