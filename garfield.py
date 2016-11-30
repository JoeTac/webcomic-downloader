from comic import Comic
from os.path import join, expanduser

def generateUrl(year, month, day):
	return "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/%04d/%04d-%02d-%02d.gif" % (year, year, month, day)
def generateFilename(year, month, day):
	return "%04d-%02d-%02d.gif" % (year, month, day)

garfield = Comic({
	'root': join(expanduser("~"), "Desktop", "comics"),
	'name': 'Garfield',
	'day': 19,
	'month': 6,
	'year': 1978,
	'url': generateUrl,
	'filename': generateFilename,
})

garfield.mainloop()