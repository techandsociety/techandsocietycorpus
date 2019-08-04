import requests
from bs4 import BeautifulSoup

import sys

url = sys.argv[1]
file_name = sys.argv[2]

response = requests.get(url)
doc = BeautifulSoup(response.text, 'html.parser')

def passes_text_filter(s):
	banned_patterns = [':"', '!function', '==', 'if (', '(func', 'translate(', 'padding:', 'display:', '\n']
	for p in banned_patterns:
		if p in s:
			return False
	parts = s.split(' ')
	if 'July' in parts:
		return True

	return True

f = open(file_name,"w+")
f.write(url + '\n')

f.write('\tdownloaded\n')
import datetime
f.write('\t\t' + str(datetime.datetime.now()) + '\n')

f.write('\thighlights\n')

f.write('\ttext\n')
def recursive_print(node):
		if hasattr(node, 'children'):
			for child in node.children:
				recursive_print(child)
		else:
			short_node = node.encode('utf-8').strip()
			if passes_text_filter(short_node) and len(short_node) > 0:
				f.write('\t\t' + short_node + '\n')

recursive_print(doc)
f.close()


