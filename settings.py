import os

def queries_of_interest():
	"""Queries of interest.
	These are the queries that we are tracking in v1 release.
	"""
	return [
		"donald trump",
		"joe biden",
		"kamala harris",
		"elizabeth warren",
		"hillary clinton",
		"ilhan omar",
		"andrew yang",
		"bernie sanders",
		"climate change",
	]

def git_path():
	"""Path to the root of the git repository that this file is in.
	"""
	return os.environ['TECHANDSOCIETY_GIT_PATH']

def git_data_path():
	"""Path to "git-tracked" data.
	This is for post-processed data. Because version-controlled data is
	expensive, this should be used to story only refined data.
	"""
	return os.path.join(git_path(), 'data')

def output_image_path():
	"""Path to the directory where graphs are written.
	These don't have to be checked in.
	"""
	return os.environ['TECHANDSOCIETY_OUTPUT_IMAGE_PATH']

def raw_data_path():
	"""Path to "raw" data.
	This is for pre-processed data. This stores a more complete, less processed
	version of the data. If product servers we don't control change, our
	processing tools might fail. So, we want to still store the more raw data, in
	case we need to recover.
	"""
	if not 'TECHANDSOCIETY_RAW_DATA_PATH' in os.environ:
		with open('/tmp/record.log', 'a') as log_file:
			log_file.write(str(os.environ) + '\n')
	return os.environ['TECHANDSOCIETY_RAW_DATA_PATH']
