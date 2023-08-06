#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, re, os, operator, argparse, argcomplete, json

from datetime import *
from subprocess import Popen, PIPE

from GoldenChild.xpath import *
from Perdy.parser import *
from Perdy.eddo import *

files = []
elements = {}
patterns = []
pairs = {}
dump = None
leader = ''
horizon = ''

lep = re.compile(
	'^\[(\d+)/(\d+)/(\d+)\s(\d+):(\d+):(\d+):(\d+)\s(\S+)\]\s([0-9a-f]{8})\s(.*)$')
sep = re.compile('^([^<]*)(<.*)$')
cdp = re.compile('^<!\[CDATA\[(.*)\]\]>$')

dsp = '%Y-%m-%d'
tsp = '%H-%M-%S.%f'


def argue():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-v', '--verbose', action='store_true', help='versbose mode')
	parser.add_argument(
		'-b',
		'--horizon',
		action='store_true',
		help='horizontal bar between messages')
	parser.add_argument(
		'-c', '--colour', action='store_true', help='show in colour')
	parser.add_argument(
		'-s', '--stubb', action='store_true', help='stub out date time stamp')
	parser.add_argument(
		'-R',
		'--rootattr',
		action='store_true',
		help='format only root xml attributes')
	parser.add_argument(
		'-a', '--attribute', action='store_true', help='format xml attributes')
	parser.add_argument(
		'-u', '--usdate', action='store_true', help='us date format')
	parser.add_argument(
		'-t', '--text', action='store_true', help='text xpath output')
	parser.add_argument(
		'-P', '--pipe', action='store', help='pipe input from command')
	parser.add_argument(
		'-e', '--element', action='store', help='xml element match', nargs='*')
	parser.add_argument(
		'-q', '--quit', action='store', help='quit on this if found')
	parser.add_argument(
		'-x', '--xpath', action='store', help='xpath on xml element')
	parser.add_argument('-d', '--dir', action='store', help='dump to directory')
	parser.add_argument(
		'-f', '--file', action='store', help='dump to file suffix')
	parser.add_argument(
		'-r', '--regex', action='store', help='regex patter', nargs='*')
	parser.add_argument(
		'-p', '--pair', action='store', help='pair of start:end tags', nargs='*')
	parser.add_argument(
		'-i', '--files', action='store', help='the files to log', nargs='*')

	argcomplete.autocomplete(parser)
	return parser.parse_args()


def getElements(a):
	global elements
	elements = {'start': [], 'end': []}
	if not a:
		return
	for e in a:
		elements['start'].append(re.compile('.*<%s(|\s.*)(|\/)>.*' % (e)))
		elements['end'].append(re.compile('.*<(/%s|%s/)>.*' % (e, e)))
	if args.verbose:
		print('elements=')
		for key in list(elements.keys()):
			print('\t%s' % key)
			for r in elements[key]:
				print('\t\t%s' % r.pattern)
	return


def getPatterns(a):
	global patterns
	patterns = []
	if not a:
		return
	for p in a:
		patterns.append(re.compile('.*%s.*' % (p)))
	if args.verbose:
		print('patterns=')
		for p in patterns:
			print('\t%s' % p.pattern)

	return


def getPairs(a):
	global pairs
	pairs = {'start': [], 'end': []}
	if not a:
		return
	for se in a:
		p = se.split(':')
		if len(p) > 1:
			pairs['start'].append(re.compile('.*%s.*' % (p[0])))
			pairs['end'].append(re.compile('.*%s.*' % (p[1])))
	if args.verbose:
		print('pairs=')
		for key in list(pairs.keys()):
			print('\t%s' % key)
			for r in pairs[key]:
				print('\t\t%s' % r.pattern)
	return


def processLine(line):
	global prints, xml, leader, dt, thread, lm
	if args.verbose:
		print(line)

	lm = lep.match(line)
	if lm:
		if args.usdate:
			months = int(lm.group(1))
			days = int(lm.group(2))
		else:
			days = int(lm.group(1))
			months = int(lm.group(2))
		years = int(lm.group(3))
		hours = int(lm.group(4))
		minutes = int(lm.group(5))
		seconds = int(lm.group(6))
		milisecs = int(lm.group(7))
		timezone = lm.group(8)
		dt = datetime(years, months, days, hours, minutes, seconds, milisecs)
		thread = lm.group(9)
		leader = lm.group(10)

	for re in patterns:
		m = re.match(line)
		if m:
			if len(m.groups()) > 0:
				if horizon:
					sys.stdout.write('%s\n' % horizon)

				dumpIfDump(m.group(1))
				sys.stdout.flush()
			else:
				dumpIfDump(line)
				sys.stdout.flush()
	for re in elements['start'] + pairs['start']:
		if re.match(line):
			prints = True
			if re in elements['start']:
				m = sep.match(line)
				if m:
					xml = ''
					line = m.group(2)
					if '/>' in line:
						if '<' in leader:
							i = leader.index('<')
							leader = leader[:i]
						printXML(line)
	if prints:
		if xml != None:
			xml += line
		else:
			if lm:
				sys.stdout.write('%s %s %s\n' % (dt, thread, leader))
			else:
				sys.stdout.write(line)
			sys.stdout.flush()
	for re in elements['end'] + pairs['end']:
		if re.match(line):
			prints = False
			if re in elements['end']:
				if xml:
					while xml[len(xml) - 1] != '>':
						xml = xml[0:-1]
					printXML(xml)
				xml = None
	sys.stdout.flush()
	if args.quit:
		if quitPattern.match(line):
			sys.stderr.write('quitting on match\n')
			return True
	return False


def printXML(xml):
	global leader, horizon
	if args.xpath:
		try:
			(doc, ctx) = getContextFromString(xml)
			for r in ctx.xpathEval(args.xpath):
				if args.text:
					dumpIfDump(r.content)
				else:
					printSnippetXML('%s' % r)
		except:
			None  #print xml
	else:
		printSnippetXML(xml)
	return


def getDumpFP():
	global dump
	fn = ''
	if args.dir:
		fn += '%s/' % args.dir.rstrip('/')
	fn += '%s' % datetime.utcnow().strftime('%s.%s' % (dsp, tsp))
	if args.file:
		fn += '.%s' % args.file
	print('%s' % fn)
	fp = open(fn, 'w')
	return fp


def dumpIfDump(text):
	global dump
	if dump:
		fp = getDumpFP()
		fp.write(text)
		fp.close()
	else:
		print(text)
	return


def printSnippetXML(xml):
	global dump
	if horizon:
		sys.stdout.write('%s\n' % horizon)
		sys.stdout.flush()
	if lm and not args.stubb:
		sys.stdout.write('%s %s %s\n' % (dt, thread, leader))
		sys.stdout.flush()
	if dump:
		fp = getDumpFP()
	else:
		fp = sys.stdout
	myParser = MyParser(
		colour=args.colour, rformat=args.rootattr, areturn=args.attribute, output=fp)
	if args.verbose:
		sys.stdout.write('xml=%s' % xml)
	try:
		myParser.parser.Parse(xml)
	except:
		while xml[:len(xml) - 1] == '\n':
			xml = xml.rtrim()
		cdm = cdp.match(xml)
		if cdm:
			xml = cdm.group(1)
		sys.stdout.write('< %s\n' % xml)
	del myParser
	if dump:
		fp.close()
	return


def main():
	global args, quitPattern, prints, files, xml, horizon, dump

	args = argue()

	prints = False
	xml = None

	if args.horizon:
		horizon = buildHorizon()

	if args.element and not args.xpath:
		args.xpath = '/'

	dump = (args.file or args.dir)
	if dump:
		args.colour = False

	if args.dir:
		if not os.path.isdir(args.dir):
			os.mkdir(args.dir)

	files = args.files

	getElements(args.element)
	getPatterns(args.regex)
	getPairs(args.pair)

	if args.quit:
		quitPattern = re.compile('^.*%s.*$' % args.quit)

	if args.pipe:
		process = Popen(args.pipe, shell=True, stdout=PIPE)
		while True:
			line = process.stdout.readline()
			if not line:
				break
			line = line.rstrip('\n').rstrip('\r')
			if processLine(line):
				del process
				break
	elif len(files) == 0:
		while sys.stdin:
			line = sys.stdin.readline()
			if processLine(line): quit()
			sys.stdout.flush()
	else:
		for f in files:
			if os.path.isfile(f):
				sys.stderr.write('< %s\n' % f)
				fp = open(f)
				for line in fp.readlines():
					if processLine(line): quit()
				fp.close()
			else:
				print('file %s doesn\'t exist' % f)

	return


if __name__ == '__main__': main()


