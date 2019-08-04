from ts_util import *
from collections import defaultdict
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import settings

Deref = False
Order = FileOrders.OLDEST
DontRegenerate = True

def GetOutputFilename(query_term, fname):
	query_parts = query_term.split(' ')
	fname_tail = fname.split('/')[-1]
	result = os.path.join(settings.git_data_path(), fname_tail + '.json')
	return result
def MakeDataset(query_term):
	query_parts = query_term.split(' ')
	escaped_query_term = '%20'.join(query_parts)
	matches = GetFilesMatching(
		['type=news.query=' + escaped_query_term + '.', ':00:'],
		settings.raw_data_path(),
		Order
		)
	def DereferenceLink(google_url):
		response = requests.get(google_url)
		soup = BeautifulSoup(response.text, 'html.parser')
		encoded = soup.prettify().encode(encoding='UTF-8',errors='strict')
		lines = encoded.split('\n')
		for link in soup.find_all('meta'):
			prop = link.get('property')
			if prop == 'og:url':
				return link.get('content')
			if prop == 'twitter:url':
				return link.get('content')
		return 'url not resolved'
	total_lines = 0
	for idx, fname in enumerate(matches):
		output_name = GetOutputFilename(query_term, fname)
		if os.path.exists(output_name) and DontRegenerate:
			# print('skipping', output_name)
			continue
		else:
			print('doing', output_name)
		result = GetAnalyzerResult(fname)
		json_result = []
		for jdx in range(len(result.sites)):
			google_url = result.urls[jdx]
			parts = [
				fname.split('date=')[-1], idx, result.sites[jdx], result.titles[jdx], google_url
				]
			obj = {
				'date' : fname.split('date=')[-1],
				'idx' : jdx,
				'publication' : result.sites[jdx],
				'title' : result.titles[jdx],
				'google_url' : google_url,
				'query' : query_term,
			}
			if Deref:
				obj['url'] = DereferenceLink(google_url)
			json_result.append(obj)
			total_lines += 1
		with open(output_name, "w") as write_file:
			json.dump(json_result, write_file, indent = 2)
	print(query_term, total_lines, len(matches))
if __name__ == "__main__":
	for query_term in settings.queries_of_interest():
		MakeDataset(query_term)
