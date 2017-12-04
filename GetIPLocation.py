#! /usr/bin/python

import sys
import socket
import urllib
import gzip
import os

try:
		import pygeoip
except ImportError:
		print '[!] Failed to Import pygeoip'
		try:
				import pip
				pip.main(['install', '-q', 'pygeoip'])
				import pygeoip
				print 'DONE'
		except Exception:
				print '[*]FAIL'
				sys.exit(1)
				
class Locater(object):
	def __init__(self, url=False, ip=False, datfile=False):
		self.url = url
		self.ip = ip
		self.datfile = datfile
		self.target = ''
		print 'in the init function'
	
	def check_database(self):
		if not self.datfile:
			self.datfile = '/usr/share/GeoIP/GeoLiteCity.dat'
			print 'Found the DB'
		else:
			if not os.path.isfile(self.datfile):
				print '[*]Failed to detect specified Database'
				sys.exit(1)
			else:
				return
		if not os.path.isfile(self.datfile):
			print '[*]Default database detection failed'
			print '[*]Attempting to auto install database'
			sys.stdout.flush()
			if not os.path.isdir('/usr/share/GeoIP'):
				os.makedirs('/usr/share/GeoIP')
			try:
				urllib.urlretrieve('http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz', '/usr/share/GeoIP/GeoLiteCity.dat.gz')
			except Exception:
				print '[FAIL]'
				print '[!] Failed to Download Database'
				sys.exit(1)
				
		try:
			with gzip.open('/usr/share/GeoIP/GeoLiteCity.dat.gz', 'rb') as compressed_dat:
				with open('/usr/share/GeoIP/GeoLiteCity.dat', 'wb') as new_dat:
					new_dat.write(compressed_dat.read())
		
		except IOError:
			print '[FAIL]'
			print '[!] Failed to Decompress Database'
			sys.exit(1)
		os.remove('/usr/share/GeoIP/GeoLiteCity.dat.gz')
		print '[DONE]\n'
		
	def query(self):
		if not not 	self.url:
			print '[*] Translating %s: ' %(self.url),
			sys.stdout.flush()
			try:
				self.target += socket.gethostbyname(self.url)
				print self.target
			except Exception:
				print '\n[!]Failed to resolve URL'
				return
		else:
			self.target += self.ip
		try:
			print '[*] Querying for Records of %s...\n' %(self.target)
			query_obj = pygeoip.GeoIP(self.datfile)
			for key, val in query_obj.record_by_addr(self.target).items():
				print '%s: %s' %(key, val)
			print '\n[*]Query Complete!'
		except Exception:
			print '\n[!] Failed to Retrieve Records'
			return

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = 'IP Geolocation Tool')
	parser.add_argument('--url', help='Locate an IP based on a URL', action='store', default=False, dest='url')
	parser.add_argument('-t', '--target', help='Locate the specified IP', action='store', default=False, dest='ip')
	parser.add_argument('--dat', help='Custom Database Filepath', action='store', default=False, dest='datfile')
	args = parser.parse_args()

if ((not not args.url) and (not not args.ip)) or ((not args.url) and (not args.ip)):
	parser.error('invalid target specification')

try:
	Locater_object = Locater(url=args.url, ip=args.ip, datfile=args.datfile)
	Locater_object.check_database()
	Locater_object.query()
	os.remove('/usr/share/GeoIP/GeoLiteCity.dat')
except Exception:
	print '\n[!]An unknown error Occured'
	sys.exit(1)
except KeyboardInterrupt:
	print '\n\n[!]Unexpected User interrupt'
	sys.exit(1)
			
				
