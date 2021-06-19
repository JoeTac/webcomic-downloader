import urllib.request
import os.path
import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

i = 0
url_pattern = "http://sssscomic.com/adv2_comicpages/page_{0:d}.jpg"
file_pattern = "{0:04d}.jpg"
save_path = "comic/adventure 2"
progress = "Downloading {0}..."
zipping = "Writing cbz [{0}]..."

chapters = {
	"Chapter 01": 33,
	"Chapter 02": 70,
	"Chapter 03": 90,
	"Chapter 04": 111,
	"Chapter 05": 152,
	"Chapter 06": 179,
	"Chapter 07": 214,
	"Chapter 08": 259,
	"Chapter 09": 297,
	"Chapter 10": 322,
	"Chapter 11": 355,
	"Chapter 12": 384,
	"Chapter 13": 0,
	"Chapter 14": 0,
	"Chapter 15": 0,
	"Chapter 16": 0,
	"Chapter 17": 0,
	"Chapter 18": 0,
	"Chapter 19": 0,
	"Chapter 20": 0,
	"Chapter 21": 0,
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
