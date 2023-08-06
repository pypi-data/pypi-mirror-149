#!/usr/bin/env python3

import os, re, sys
from datetime import datetime, timedelta
from dateutil import tz


class Yokel(object):
	'''
    datetime fixerupper to local
    '''
	dts = '%Y-%m-%d %H:%M:%S'
	its = '%a, %d %b %Y %H:%M:%S'
	p = re.compile('^(.*)\s([\+\-])(\d\d)(\d\d)$')
	gmt = tz.gettz('UTC')

	def __init__(self, tz=tz.tzlocal()):
		self.local = tz

	def time(self, dt):
		m = self.p.match(dt)
		if m:
			delta = m.group(2)
			td = timedelta(hours=int(m.group(3)), minutes=int(m.group(4)))
			d = datetime.strptime(m.group(1), self.its).replace(tzinfo=self.gmt)
			if delta == '+':
				d = d - td
			if delta == '-':
				d = d + td
			return d.astimezone(self.local)
		return


if __name__ == '__main__':
	yokel = Yokel()

	times = ['Thu, 30 Mar 2017 18:48:06 +1000', 'Thu, 30 Mar 2017 10:31:37 +0200']

	for time in times:
		here = yokel.time(time)
		print('%s -> %s' % (time, here.strftime(yokel.dts)))


