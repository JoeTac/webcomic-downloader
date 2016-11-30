from datetime import date
from calendar import monthrange, month_name
from os import mkdir, remove
from os.path import exists, join
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from urllib import request
from comic.i18n import text
import zlib

def newdir(dirname):
	if exists(dirname)==False:
		mkdir(dirname)

class Comic:
	def __init__(self, args={}):
		self.name = args['name']
		self.url = args['url']
		self.filename = args['filename']
		self.day = int(args['day'])
		self.month = int(args['month'])
		self.year = int(args['year'])

		if 'compression' in args:
			self.compression = args['compression']
		else:
			self.compression = ZIP_DEFLATED

		if 'root' in args:
			self.root = args['root']
		else:
			self.root = ""

		if 'subdir' in args:
			self.subdir = args['subdir']
		else:
			self.subdir = self.defaultSubdir

		if 'zfile' in args:
			self.zfile = args['zfile']
		else:
			self.zfile = self.defaultZfile

		if 'progress' in args:
			self.progress = args['progress']
		else:
			self.progress = self.defaultProgress

	def mainloop(self):
		self.progress(text['resuming'])
		newdir(self.name)

		year = self.year
		month = self.month
		day = self.day
		while True:
			output = join(self.filepath(year), self.zfile(year, month))
			if exists(output)==False:
				break
			else:
				day = 1

			month = month + 1
			if month>12:
				month = 1
				year = year + 1

		files = []
		today = date.today()
		newdir(self.root)
		newdir(join(self.root, self.name))
		newdir(self.filepath(year))
		while True:
			last_day = monthrange(year, month)[1]
			if year==today.year and month==today.month and day>today.day:
				break

			filename = self.filename(year, month, day)
			save_location = join(self.filepath(), filename)
			files.append(filename)

			if exists(save_location)==False:
				url = self.url(year, month, day)
				self.progress(text['downloading'] % (url))
				
				rhttp = request.urlopen(url)
				if rhttp.reason!='OK':
					self.progress(text['error'] % (rhttp.reason))
					continue
				
				bytes = rhttp.read()
				f = open(save_location, "wb")
				f.write(bytes)
				f.close()
				rhttp.close()

			day = day + 1
			if day>last_day:
				self.createZipfile(files, year, month)
				files = []
				break

				day = 1
				month = month + 1
				if month>12:
					month = 1
					year = year + 1

		self.progress(text['complete'])

	def createZipfile(self, files, year, month):
		self.progress(text['compressing'])
		zpath = self.filepath(year)
		newdir(zpath)
		zfile = self.zfile(year, month)

		zf = ZipFile(join(zpath, zfile), 'w', self.compression)
		for f in files:
			fpath = join(self.filepath(), f)
			zf.write(fpath, f)
			remove(fpath)
		zf.close()

	def filepath(self, year=0):
		if(year>0):
			return join(self.root, self.name, self.subdir(year))
		else:
			return join(self.root, self.name)

	#Customizable Methods
	def defaultSubdir(self, year):
		return str(year)
	def defaultZfile(self, year, month):
		return "%02d - %s %04d.cbz" % (month, month_name[month], year)
	def defaultProgress(self, message):
		print(message)
