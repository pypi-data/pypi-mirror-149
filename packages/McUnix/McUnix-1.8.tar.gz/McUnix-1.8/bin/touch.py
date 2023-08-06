#!/usr/bin/env python3

import sys, os, re, arrow, time, pytz
from datetime import datetime
from dateutil import tz

gmt = tz.gettz('UTC')
ltz = tz.gettz('AEST')

dts_date = '(YYYY)[/\-](MM)[/\-](DD)'
dts_time = '(HH)[:\-](mm)[\-](ss)'
dts = [ '%s[ _]%s'%(dts_date,dts_time), dts_date ]


def to_re(dts):
	for token in 'YMDHms':
		dts = dts.replace(token, '\d')
	return re.compile('.*%s.*' % dts)


dts_p = list(map(to_re, dts))

files = sys.argv[1:]
if len(files) == 0:
	files = os.listdir('.')

for file in files:
	sys.stdout.write(file)

	for p in dts_p:
		m = p.match(file)
		if m:
			if len(m.groups()) == 6:
				(Y,M,D,h,m,s) = tuple(list(m.groups()))
			else:
				(Y,M,D,h,m,s) = tuple(list(m.groups())+['00','00','00'])
			dts = '%s-%s-%s %s:%s:%s'%(Y,M,D,h,m,s)
			at = arrow.get(dts)
			nt = at.naive.replace(tzinfo=ltz)
			ut = time.mktime(nt.timetuple())
			if ut != os.stat(file).st_mtime:
				os.utime(file, (ut, ut))
				sys.stdout.write(' -> %s' % nt.astimezone(ltz))

			break

	sys.stdout.write('\n')

