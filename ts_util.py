from os import listdir
from os.path import isfile, join
import sys
from collections import defaultdict
import numpy as np
from enum import Enum
import random
import requests
from bs4 import BeautifulSoup

class FileOrders(Enum):
	OLDEST = 1
	NEWEST = 2
	RANDOM = 3
class AnalyzerResult(object):
	def __init__(self):
		self.site_counts = defaultdict(int)
		self.site_titles = defaultdict(list)
		self.site_urls = defaultdict(list)
		self.sites = []
		self.titles = []
		self.urls = []
def GetAnalyzerResult(file_name):
	with open(file_name, 'r') as in_file:
		contents = in_file.readlines()
	sites = defaultdict(int)
	last_title = None
	last_url = None
	result = AnalyzerResult()
	for idx, line in enumerate(contents):
		if idx < len(contents) - 1:
			next_line = contents[idx + 1].strip()
		else:
			next_line = None
		if 'DY5T1d' in line:
			last_title = next_line
			url = line.split('"')[3]
			last_url = 'http://news.google.com/' + url
		if 'wEwyrc AVN2gc uQIVzc Sksgp' in line:
			name = next_line
			result.site_counts[name] += 1
			result.site_titles[name].append(last_title)
			result.site_urls[name].append(last_url)
			result.sites.append(name)
			result.titles.append(last_title)
			result.urls.append(last_url)
	return result
def SortByKey(s):
	return s[0]
def SortByValue(s):
	return -1 * s[1]
def SortByValueLen(s):
	return -1 * len(s[1])
def PrintSortedMap(m):
	s = sorted(list(m.items()), key =SortByValue);
	print(s)
def GetSortedMap(m):
	return [k for k, v in sorted(list(m.items()), key =SortByValue)]
def GetSortedMapPairs(m):
	return sorted(list(m.items()), key =SortByValue)
def ToString(parts):
	str_parts = [str(p) for p in parts]
	return ','.join(str_parts)
class MergeResult(object):
	def __init__(self):
		self.total_sites = 0
		self.site_counts = defaultdict(list)
		self.site_mean = {}
		self.site_std = {}
	def ToString(self):
		return ToString([self.total_sites, self.site_counts, self.site_mean, self.site_std])
def MergeAnalyzerResults(results):
	merge_result = MergeResult()
	for result in results:
		for site, count in result.site_counts.items():
			merge_result.total_sites += count
			merge_result.site_counts[site].append(count)
	for k in merge_result.site_counts:
		merge_result.site_mean[k] = np.mean(merge_result.site_counts[k])
		merge_result.site_std[k] = np.std(merge_result.site_counts[k])
	return merge_result
def GetFilesMatching(filters, directory, order, max_matches = None):
	matches = []
	for fn in listdir(directory):
		in_all = True
		for filter_ in filters:
			if not filter_ in fn:
				in_all=False
		if in_all:
			matches.append(fn)
			
	if order == FileOrders.OLDEST:
		sorted_matches = sorted(matches)
	elif order == FileOrders.NEWEST:
		sorted_matches = list(reversed(sorted(matches)))
	elif order == FileOrders.NEWEST:
		sorted_matches = list(random.shuffle(matches))
	else:
		sorted_matches = matches
	result = []
	if max_matches:
		use_matches = sorted_matches[:max_matches]
	else:
		use_matches = sorted_matches
	for idx, fname in enumerate(use_matches):
		result.append(join(directory, fname))
	return result
