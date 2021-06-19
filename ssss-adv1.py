import urllib.request
import os.path
import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

i = 0
url_pattern = "http://www.sssscomic.com/comicpages/{0:d}.jpg"
file_pattern = "{0:04d}.jpg"
save_path = "comic/adventure 1"
progress = "Downloading {0}..."
zipping = "Writing cbz [{0}]..."

chapters = {
	"Prologue":   68,
	"Chapter 01": 119,
	"Chapter 02": 141,
	"Chapter 03": 178,
	"Chapter 04": 222,
	"Chapter 05": 276,
	"Chapter 06": 300,
	"Chapter 07": 363,
	"Chapter 08": 412,
	"Chapter 09": 437,
	"Chapter 10": 509,
	"Chapter 11": 585,
	"Chapter 12": 629,
	"Chapter 13": 658,
	"Chapter 14": 687,
	"Chapter 15": 752,
	"Chapter 16": 782,
	"Chapter 17": 814,
	"Chapter 18": 863,
	"Chapter 19": 899,
	"Chapter 20": 924,
	"Chapter 21": 975,
	"Chapter 22": 0,
}

if not os.path.exists(save_path):
    os.makedirs(save_path)

for chapter in chapters.items():
	cbz = "Stand Still. Stay Silent - " + chapter[0] + ".cbz"
	if ( os.path.exists(cbz) ):
		continue
	
	startIndex = i + 1
	while i<chapter[1] or chapter[1]==0:
		i = i + 1
		url = url_pattern.format(i)
		file = file_pattern.format(i)
		save = save_path + "/" + file

		if os.path.exists(save):
			continue

		print(progress.format(url))
		try:
			urllib.request.urlretrieve(url, save)
		except:
			print("Reached of comic pages.")
			break

	if i==chapter[1]:
		print(zipping.format(chapter[0]))
		zf = zipfile.ZipFile(cbz, mode='w')
		for j in range(startIndex, chapter[1]+1):
			file = file_pattern.format(j)
			save = save_path + "/" + file
			zf.write(save, compress_type=compression, arcname=file)
		zf.close()
