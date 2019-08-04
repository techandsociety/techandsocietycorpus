# https://news.google.com/search?q=peter%20thiel&hl=en-US&gl=US&ceid=US%3Aen
import datetime
import pipeline.recursive_download
import settings
import sys
BaseDir = settings.raw_data_path()
query = sys.argv[1]
NumPages = int(sys.argv[2])
query_parts = query.split(' ')
time_stamp = datetime.datetime.now().isoformat()
for page_index in range(0, NumPages):
	page_part = 10 * page_index
	query_part = '+'.join(query_parts)
	url = 'https://www.google.com/search?q=%(query_part)s&start=%(page_part)d' % {
		'query_part' : query_part,
		'page_part' : page_part,
	}
	file_name = '%(base_dir)s/query=%(query_part)s.start=%(page_part)d.date=%(date_part)s' % {
		'base_dir' : BaseDir,
		'query_part' : query_part,
		'date_part' : time_stamp,
		'page_part' : page_part,
	}
	pipeline.recursive_download.DownloadUrl(url, file_name)
