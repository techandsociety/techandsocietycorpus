import datetime
import os
import requests
import settings
import sys
from bs4 import BeautifulSoup
def DownloadUrl(url, file_name):
	print('DownloadUrl', url, file_name)
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	encoded = soup.prettify().encode(encoding='UTF-8',errors='strict')
	lines = encoded.split('\n')
	def ParseLine(line):
		for idx, char in enumerate(line):
			if char != ' ':
				return idx, line[idx:]
		return len(line), ''
	def TabIndent(pair):
		buf = ''
		for i in range(0, pair[0]):
			buf += '\t'
		buf += pair[1]
		buf += '\n'
		return buf
	pairs = []
	last_tag_prefix_len = -1
	style_block = False
	for line in lines:
		tuple_ = ParseLine(line)
		[prefix_len, payload] = tuple_
		if not payload.strip():
			continue
		if payload.startswith('</'):
			last_tag_prefix_len = prefix_len - 1
			style_block = False
			continue
		if payload.startswith('<'):
			last_tag_prefix_len = prefix_len
			this_prefix_len = prefix_len

			if payload.startswith('<style'):
				style_block = True
			if payload.startswith('<script'):
				style_block = True
			if payload.startswith('<meta'):
				style_block = True
		else:
			this_prefix_len = last_tag_prefix_len + 1
		
		if style_block:
			continue

		pairs.append([this_prefix_len, payload])

	with open(file_name, 'w') as out_file:
		for pair in pairs:
			out_line = TabIndent(pair)
			out_file.write(out_line)
if __name__ == "__main__":
	url = sys.argv[1]
	def FileNameFromUrl(url):
		buf = ''
		for c in url:
			if c >= 'A' and c <= 'Z':
				buf += c
			elif c >= 'a' and c <= 'z':
				buf += c
			elif c >= '0' and c <= '9':
				buf += c
			else:
				buf += '_'
		return buf
	sanitized_url = FileNameFromUrl(url)
	base_dir = settings.raw_data_path()
	time_stamp = datetime.datetime.now().isoformat()
	local_dir = base_dir + '/' + sanitized_url
	try:
		os.mkdir(local_dir)
	except OSError:
		print('already exists: ' + local_dir)
	file_name = local_dir + '/' + time_stamp
	print('write to:', file_name)
	DownloadUrl(url, file_name)
