import csv
import datetime
import json
import os
import sys
import ts_util

def ReadTuples(data_fname, label_fname, study_code, legend_file):
	legend = [ p[0] for p in ts_util.GetOrderedLegendFromFile(legend_file) ] + ['n']
	data_rows = []
	with open(data_fname) as json_file:
		data_rows = json.load(json_file)
	try:
		label_rows = []
		with open(label_fname) as json_file:
			label_rows = json.load(json_file)
	except ValueError:
		pass
	labeled_urls = set()
	needed_urls = set()
	for label_row in label_rows:
		labeled_urls.add(label_row['google_url']) 
	for data_row in data_rows:
		needed_urls.add(data_row['google_url'])
	def GetJsonWithUrl(url):
		for row in data_rows:
			if row['google_url'] == url:
				return row
		return None
	def GetUrlSet(rows):
		return set([row['google_url'] for row in rows])
	while GetUrlSet(data_rows) - GetUrlSet(label_rows):
		diff = GetUrlSet(data_rows) - GetUrlSet(label_rows)
		url0 = list(diff)[0]
		row0 = GetJsonWithUrl(url0)
		# print(row0)
		print('\n')
		print(len(data_rows), len(label_rows))
		print(json.dumps(row0, indent = 2))
		for idx, l in enumerate(legend):
			print(idx + 1, l) # 1 vs 0 offset
		response = raw_input("> ")
		parts = response.split(' ')
		note = None
		if len(parts) > 1:
			note = ' '.join(parts[1:])
		if parts[0] in legend:
			response = parts[0]
		else:
			int_response = int(parts[0])
			response = legend[int_response - 1] # 1 vs 0 offset
		row_copy = dict(row0)
		if not 'ratings' in row_copy:
			row_copy['ratings'] = {}
		row_copy['ratings'][study_code] = response
		if note:
			if not 'notes' in row_copy:
				row_copy['notes'] = {}
			row_copy['notes'][study_code] = note
		print(json.dumps(row_copy, indent = 2))
		label_rows.append(row_copy)
		with open(label_fname, "w") as write_file:
			json.dump(label_rows, write_file, indent = 2)

if __name__ == "__main__":
	data_fname = sys.argv[1] 
	label_fname = sys.argv[2]
	study_code = sys.argv[3]
	legend_file = sys.argv[4]
	ReadTuples(data_fname, label_fname, study_code, legend_file)
