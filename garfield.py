from urllib import request
from os import mkdir
from os.path import isdir, exists, join
from datetime import date
from calendar import monthrange, month_name
from time import sleep

start_yr = 1978
start_mt = 6
start_dy = 19

server = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/%04d/%04d-%02d-%02d.gif"
root_dir = "Garfield"
sleep_time = 0.5

def newdir(dir):
	if isdir(dir)==False:
		mkdir(dir)

today = date.today()
day = start_dy
month = start_mt
year = start_yr

newdir(root_dir)
newdir(join(root_dir, str(year)))
newdir(join(root_dir, str(year), month_name[month]))
while True:
	last_day = monthrange(year, month)[1]
	if year==today.year:
		break

	url = server % (year, year, month, day)
	rhttp = request.urlopen(url)
	
	print("Downloading %s" % url)

	if rhttp.reason!='OK':
		print("ERROR: " + rhttp.reason)

		f = open(join(root_dir, "errors.log"), "a")
		f.write(rhttp.reason + " " + url)
		f.close()
		continue
	
	bytes = rhttp.read()
	fname = "%04d-%02d-%02d.gif" % (year, month, day)
	f = open(join(root_dir, str(year), month_name[month], fname), "wb")
	f.write(bytes)
	f.close()
	sleep(sleep_time)

	day = day + 1
	if day>last_day:
		day = 1
		month = month + 1
		if month>12:
			month = 1
			year = year + 1
			newdir(join(root_dir, str(year)))
		
		newdir(join(root_dir, str(year), month_name[month]))
