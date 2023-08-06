#!/usr/bin/env python3

import os, re, sys, urllib.request, urllib.parse, urllib.error

for arg in sys.argv[1:]:
	file = os.path.abspath(arg)
	print('file://%s' % (urllib.parse.quote(file)))


