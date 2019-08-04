def GetFieldRecursive(row, parts):
	curr = row
	for part in parts:
		if part in row:
			curr = row[part]
	return curr
def RecursiveSet(row, path, value):
	parts = path.split('.')
	curr = row
	for part in parts[:-1]:
		if part in curr:
			curr = curr[part]
		else:
			curr[part] = {}
			curr = curr[part]
	curr[parts[-1]] = value
def RecursiveRead(row, path):
	parts = path.split('.')
	penultimate = GetFieldRecursive(row, parts[:-1])
	if parts[-1] in penultimate:
		return penultimate[parts[-1]] 
	else:
		return None
def RecursiveDelete(row, path):
	parts = path.split('.')
	penultimate = GetFieldRecursive(row, parts[:-1])
	if parts[-1] in penultimate:
		del penultimate[parts[-1]] 
