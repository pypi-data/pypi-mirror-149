#!/usr/bin/env python3

import re, os


def findFiles(path='.', fileOrDir=True, pn='^.*$'):
	files = []
	p = re.compile(pn)
	for f in os.listdir('%s' % path):
		fp = '%s/%s' % (path.rstrip('/'), f)
		if os.path.isfile(fp):
			# is a file
			if p.match(f) and fileOrDir:
				# matches and are looking for files
				files.append(fp)
		elif os.path.isdir(fp):
			#is a dir
			if p.match(f) and not fileOrDir:
				files.append(fp)
			files += findFiles(fp, fileOrDir, pn)
	return files

