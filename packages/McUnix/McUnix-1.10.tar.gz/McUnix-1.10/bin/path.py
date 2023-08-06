#!/usr/bin/env python3

import sys, os
from collections import OrderedDict
from Baubles.Colours import Colours

colours = Colours(colour=True)

paths = ''
for key in ['BIN_PATH', 'PATH']:
	if key in list(os.environ.keys()):
		paths = os.environ[key]
		print('%s:' % key)
		break

substitutions = OrderedDict([
	('ROOT', '^'),
	('STASH_ROOT', '#'),
	('PYTHONHOME', '%'),
	('HOME', '~'),
])

for key, short in substitutions.items():
	if key in list(os.environ.keys()):
		print('%s=%s=%s' % (short, key, os.environ[key]))

for path in paths.split(':'):
	path = os.path.expanduser(path)

	if os.path.isdir(path):
		colour = colours.Green
	else:
		colour = colours.Red

	for key, short in substitutions.items():
		if key in list(os.environ.keys()) and path.startswith(os.environ[key]):
			path = path.replace(os.environ[key], short)

	print('+ %s%s%s' % (colour, path, colours.Off))


