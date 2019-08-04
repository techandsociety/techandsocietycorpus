import sys
import ts_util
from collections import defaultdict
import csv
import datetime
import json
import os
import settings
import sys

# Get all files from on an hour.
matching_files = ts_util.GetFilesMatching([':00:'], settings.git_data_path(), ts_util.FileOrders.OLDEST)

rows = []
for fn in matching_files:
	with open(fn, 'r') as infile:
		data_rows = json.load(infile)
	rows += data_rows

query_rows = defaultdict(list)
query_times = defaultdict(set)
for row in rows:
	query_rows[row['query']].append(row)
	query_times[row['query']].add(row['date'])

def ComputeGaps(time_strings):
	day_hours = []
	for idx, f in enumerate(time_strings):
		parts = f.split(':')
		time_part = parts[-3]
		dot_parts = time_part.split('.')
		date_part = dot_parts[-1]
		dash_part = date_part.split('-')[-1]
		day_hour = dash_part.split('T')
		day_hours.append(day_hour)
	result = ''
	num_gaps = 0
	for idx, dh in enumerate(day_hours):
		if idx == 0:
			continue
		last_hour = int(day_hours[idx - 1][1])
		this_hour = int(day_hours[idx][1])
		last_day = int(day_hours[idx - 1][0])
		this_day = int(day_hours[idx][0])

		if this_hour == last_hour + 1:
			pass
		elif this_hour == (last_hour + 1) % 24:
			pass
		else:
			result += str([[day_hours[idx - 1], day_hours[idx]]]) + ', '
			num_gaps += 1
	return result, num_gaps

sqt = sorted(query_times.items(), key = ts_util.SortByValueLen)
out_rows = []
for k, v in sqt:
	sv = sorted(v)
	gaps, num_gaps = ComputeGaps(sv)
	out_rows.append({
		'query' : k,
		'file_count' : len(sv),
		'start' : sv[0],
		'end' : sv[-1],
		'gaps' : gaps,
		'gap_count' : num_gaps,
	})

print(json.dumps(out_rows, indent = 2))
