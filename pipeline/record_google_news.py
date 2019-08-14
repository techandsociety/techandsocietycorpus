# https://news.google.com/search?q=peter%20thiel&hl=en-US&gl=US&ceid=US%3Aen
with open('/tmp/greg', 'a') as log_file:
	log_file.write('starting\n')
import datetime
import pipeline.recursive_download
import random
import settings
import sys
time_stamp = datetime.datetime.now().isoformat()
log_file = open('/tmp/record.log', 'a')
log_file.write('starting at ' + time_stamp + '\n')
log_file.flush()
NumPages = 1
log_file.write(str(NumPages) + '\n')
log_file.flush()
BaseDir = settings.raw_data_path()
log_file.write('BaseDir' +  BaseDir + '\n')
log_file.flush()
log_file.write('before query \n')
log_file.flush()
query = sys.argv[1]
log_file.write('after query \n')
log_file.flush()
query_parts = query.split(' ')
log_file.write('before range at ' + time_stamp + '\n')
for page_index in range(0, NumPages):
	log_file.write('page_index ' + str(page_index) + ', ' + time_stamp + '\n')
	log_file.flush()
	page_part = 10 * page_index
	query_part = '%20'.join(query_parts)
	url = """https://news.google.com/search?q=%(query_part)s&hl=en-US&gl=US&ceid=US""" % {
		'query_part' : query_part,
	}
	file_name = '%(base_dir)s/type=news.query=%(query_part)s.start=%(page_part)d.date=%(date_part)s' % {
		'base_dir' : BaseDir,
		'query_part' : query_part,
		'date_part' : time_stamp,
		'page_part' : page_part,
	}
	pipeline.recursive_download.DownloadUrl(url, file_name)
