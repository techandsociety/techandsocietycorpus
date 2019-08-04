import json
import os
import sys

file_name = sys.argv[1]

if os.path.exists(file_name):
	print ('exists')
else:
	print ('no exists, making')
	with open(file_name, 'w') as f:
		f.write('[]\n')


