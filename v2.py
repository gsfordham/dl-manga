#! /usr/bin/python3.6

#imports
import requests, sys, getopt, os, bs4

def extract_url(src):
	strands = str(src).split('/')
	url = strands[len(strands) - 1]
	
	#print(url + " from: " + src)
	
	return ((url, src))

def dl_img(path, item):
	src = item[1]
	fname = item[0]
	r = requests.get(src, stream=True)
	r.raise_for_status()
	#print(r.headers['content-type'])
	
	fitem = str(path + "/" + fname)
	with open(fitem, 'wb') as fdes:
		print("Saved: " + src + " to:\n  " + path + "/" + fname)
		for chunk in r.iter_content(chunk_size=50000):
			fdes.write(chunk)

def save_images(path, lst):
	out = ""
	err = ""
	
	#print(str(lst))
	for item in lst:
		dl_img(path, item)
	
	return (out, err)

def list_items(path, reader_list):
	out = ""
	err = ""
	lst = []
	
	for img in reader_list.find_all('img'):
		lst.append(extract_url(img.get('src')))
		
	#print(str(lst))
	out, err = save_images(path, lst)
	
	return (out, err)

def results(path, url, divin=''):
	out = ""
	err = ""
	#print(divin)
	divf = divin.strip()
	print(divf)
	
	doc = requests.get(url.strip())
	html = bs4.BeautifulSoup(doc.text, 'html.parser')
	if divf != '':
		for d in html.find_all('div'):
			#print(str(d.get('class')))
			values = d.get('class')
			if values is not None:
				for v in list(values):
					#print(v)
					if divf == v:
						#print(str(d))
						out, err = list_items(path, d)
	else:
		print(str(html.body))
	
	return (out, err)

def get_help():
	return (
		"Description:\n" +
		"A program to download the page images from online" +
		"reading material, such as manga or comics.\n\n" +
		"Usage:\n" + 
		"\n".join([
			("  -h, --help\t\t" + "Print this help message"),
			("  -v, --version\t\t" + "Prints the program version"),
			("  -u, --url\t\t" + "The URL the pages are located at"),
			("  -d, --div\t\t" + "The id of the div where the images are located\n" +
				"    [Avoids downloading of random image files]")
			])
		)

def main(argv):
	cwd = str(os.getcwd())
	out = ""
	err = ""
	end_early = False
	help = get_help()
	version = ("0.1.1")
	url = ""
	div = ""
	cls = ""
	
	opts, args = getopt.gnu_getopt(argv, "hvu:d:", ["help", "version", "url=", "div="])
	
	for o, a in opts:
		if o in ["-h", "--help"]:
			out = str(help)
			end_early = True
			break
		elif o in ["-u", "--url"]:
			url = str(a)
			#out += ("Will get pages...")
		elif o in ["-d", "--div"]:
			div = str(a)
		elif o in ["-v", "--version"]:
			out = ("Version: " + str(version))
			end_early = True
			break
		
	if not end_early and ((url.strip() != "" and div.strip() != "") or cls.strip() != ""):
		uin = input("Do you wish to download the pages located at: " + url +
			"\n  to this folder (" + cwd + ")\n" +
			"++Using the div class: " + div +
			" [y/n] ").strip()
		#print("Input received as: " + str(uin))
		if uin != "":
			if uin.lower().startswith("y"):
				r, o = results(cwd, url, div)
			elif uin.lower().startswith("n"):
				out += "Canceling."
			else:
				out += "That is an invalid response. Canceling."
	
	#print("Current directory: " + str(os.getcwd()))
	return (out)
	
print(main(sys.argv[1:]))
