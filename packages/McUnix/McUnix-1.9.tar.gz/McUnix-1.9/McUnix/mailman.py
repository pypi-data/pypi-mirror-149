#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, os, re, json, argparse, argcomplete, poplib, imaplib, smtplib, mimetypes

from datetime import datetime, timedelta
from dateutil import tz

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser

from Baubles.Colours import Colours
from McUnix.yokel import Yokel
from Spanners.Squirrel import Squirrel
from Argumental.Argue import Argue

yokel = Yokel()
squirrel = Squirrel()
args = Argue()


@args.argument(short='v', flag=True)
def verbose():
	return


#__________________________________________________________________________________________________________
@args.command(single=True, help='wrapper around the python email')
class MailMan(object):

	#......................................................................................................
	_encrypt = False


	@args.property(short='e', flag=True, help='SSL encryption')
	def encrypt(self):
		return self._encrypt

	@encrypt.setter
	def encrypt(self, value):
		self._encrypt = value

	
	#......................................................................................................
	_server = None

	@args.property(short='s', required=True, help='the server hostname')
	def server(self):
		return self._server

	@server.setter
	def server(self, value):
		self._server = value


	#......................................................................................................
	_outport = 25

	@args.property(short='o', type=int, default=_outport, help='output port')
	def outport(self):
		return self._outport

	@outport.setter
	def outport(self, value):
		self._outport = value


	#......................................................................................................
	_inport = 110

	@args.property(short='i', type=int, default=_inport, help='input port')
	def inport(self):
		return self._inport

	@inport.setter
	def inport(self, value):
		self._inport = value

	
	#......................................................................................................
	_tipe = 'POP3'

	@args.property(
		short='t', choices=['IMAP', 'POP3'], default=_tipe, help='protocol')
	def tipe(self):
		return self._tipe

	@tipe.setter
	def tipe(self, value):
		self._tipe = value

	
	#......................................................................................................
	_username = None

	@args.property(short='u', required=True, help='login username')
	def username(self):
		return self._username

	@username.setter
	def username(self, value):
		self._username = value


	#......................................................................................................
	_password = None

	@args.property(short='p', help='login password')
	def password(self):
		if not self._password:
			self.password = squirrel.get('%s:%s' % (self.server, self.username))
		return self._password

	@password.setter
	def password(self, value):
		self._password = value


	#......................................................................................................
	def payload(self, part, save=None):
		return dict(
			payload=part.get_payload(),
			filename=part.get_filename(),
			type=part.get_content_type())


	#......................................................................................................
	def process(self, message, output=None, save=None):
		parser = Parser()

		if verbose():
			print(message)

		jm = parser.parsestr(message)

		if jm:
			if verbose():
				json.dump(list(jm.keys()), sys.stderr, indent=4)

			payload = list()
			if jm.is_multipart():
				for part in jm.get_payload():
					payload.append(self.payload(part, save=save))

			jsm = dict(preamble=jm.preamble, payload=payload)

			for key in ['To', 'From', 'Subject']:
				jsm[key] = jm.get(key)

			try:
				dt = yokel.time(jm['Date'])
				jsm['Date'] = dt.strftime(yokel.dts)
			except:
				jsm['Date'] = jm['Date']

			if output:

				output.write('{:<19} {:<20} -> {:<40}\n'.format(jsm['Date'][:19], jsm[
					'From'][:20], jsm['Subject'][:55]))

		else:
			pass
			#sys.stderr.write('%s\n' % message)

		del parser

		return


	#......................................................................................................
	@args.operation(name='read')
	@args.parameter(name='delete', short='d', flag=True, help='burn after reading')
	@args.parameter(name='output', short='o', help='output to file, @=stdout')
	@args.parameter(name='save', short='s', help='save to this directory')
	@args.parameter(name='words', short='w', nargs='*', help='killing words')
	def read(self, delete=False, output=None, save=None, words=[], find=[]):
		'''
        read email from the server
        '''

		if output:
			if output == '@':
				output = sys.stdout
			else:
				output = open(output, 'w')

		found = []

		if self.tipe == 'POP3':

			if self.encrypt:
				poppy = poplib.POP3_SSL(_server(), _inport())
			else:
				poppy = poplib.POP3(self.server, self.inport)

			poppy.user(self.username)
			poppy.pass_(self.password)
			numMessages = len(poppy.list()[1])
			#sys.stderr.write('Number of messages = %d\n' % numMessages)

			for m in range(numMessages):
				#sys.stdout.write('\r%d ' % (m+1))
				message = poppy.retr(m + 1)
				parts = map(lambda x: x.decode('UTF8'), message[1])
				
				for word in find:
					if word.lower() in '\n'.join(parts).lower():
						found.append('\n'.join(parts))

				killed = any(word.lower() in '\n'.join(parts).lower() for word in words)

				try:
					self.process('\n'.join(parts), output=output, save=save)
				except:
					pass

				if delete:  # or killed:
					poppy.dele(m + 1)
					continue

			poppy.quit()

		if self.tipe == 'IMAP':

			if self.encrypt:
				eye = imaplib.IMAP4_SSL(self.server, self.inport)
			else:
				eye = imaplib.IMAP4(self.server, self.inport)

			eye.login(self.username, self.password)

			if verbose():
				json.dump(eye.list(), sys.stderr, indent=4)

			eye.select('inbox')

			tipe, data = eye.search(None, 'ALL')

			for n in data[0].split():
				num = n.decode('UTF8')
				#sys.stdout.write('\r%s ' % num)
				tipe, data = eye.fetch(num, '(RFC822)')
				message = data[0][1].decode('UTF8')
				self.process(message, output=output, save=save)

			eye.close()
			eye.logout()

		if output:
			if output is not sys.stdout:
				output.close()

		return found


	#......................................................................................................
	@args.operation(name='send')
	@args.parameter(name='fromaddr',short='f',default='eddo888@tpg.com.au',help='sender email')
	@args.parameter(name='recipients',short='t',nargs='*',required=True,help='recipient list')
	@args.parameter(name='subject', short='s', required=True, help='email subject')
	@args.parameter(name='body', short='b', required=True, help='text body')
	@args.parameter(name='preamble', short='p', help='some leading text in lieu of a body')
	@args.parameter(name='files', short='a', nargs='*', help='list of atttachments')
	def send(self,fromaddr=None,recipients=[],subject=None,body=None,preamble=None,files=[]):
		'''
        send an email

        '''

		COMMASPACE = ', '

		msg = MIMEMultipart()

		msg['Subject'] = subject
		msg['From'] = fromaddr
		msg['To'] = COMMASPACE.join(recipients)

		if preamble:
			msg.preamble = preamble

		if body == '@-':
			with sys.stdin as fp:
				body = MIMEText(fp.read())
				msg.attach(body)
		elif body.startswith('@'):
			with open(body[1:], 'r') as fp:
				body = MIMEText(fp.read())
				msg.attach(body)
		else:
			bt = MIMEText(body)
			msg.attach(bt)

		for file in files:
			# Assume we know that the image files are all in PNG format
			# Open the files in binary mode.  Let the MIMEImage class automatically
			# guess the specific image type.

			ctype, encoding = mimetypes.guess_type(file)
			if ctype is None or encoding is not None:
				# No guess could be made, or the file is encoded (compressed), so
				# use a generic bag-of-bits type.
				ctype = 'application/octet-stream'
			maintype, subtype = ctype.split('/', 1)
			if maintype == 'text':
				with open(file) as fp:
					# Note: we should handle calculating the charset
					atch = MIMEText(fp.read(), _subtype=subtype)
			elif maintype == 'image':
				with open(file, 'rb') as fp:
					atch = MIMEImage(fp.read(), _subtype=subtype)
			elif maintype == 'audio':
				with open(file, 'rb') as fp:
					atch = MIMEAudio(fp.read(), _subtype=subtype)
			else:
				with open(file, 'rb') as fp:
					atch = MIMEBase(maintype, subtype)
					atch.set_payload(fp.read())
					# Encode the payload using Base64
					encoders.encode_base64(atch)

			atch.add_header('Content-Disposition', 'attachment', filename=file)
			msg.attach(atch)

		# Send the email via our own SMTP server.
		if self.encrypt:
			s = smtplib.SMTP_SSL(self.server, self.outport)
		else:
			s = smtplib.SMTP(self.server, self.outport)

		if self.username and self.password:
			s.login(self.username, self.password)

		s.sendmail(fromaddr, msg['To'], msg.as_string())
		s.quit()

		return


#__________________________________________________________________________________________________________
if __name__ == '__main__':
	#args.parse('-s mail.tpg.com.au -u eddo8888 read -o @'.split())
	#args.parse('-e -t IMAP -s imap.gmail.com -i 993 -u david.edson@gmail.com read -o @'.split())
	results = args.execute()
	if results:
		print(result)


