import urllib.request
import random
import sys
import re
from PIL import Image, ImageFilter
from db import Database
import argparse
import json
from collections import namedtuple

genre = [
		'all',
		'hi-tech',
		'abstraction',
		'aviation',
		'city',
		'girls',
		'food',
		'painting',
		'animals',
		'games',
		'space',
		'interior',
		'cats',
		'macro',
		'miscellanea',
		'nature',
		'holidays',
		'landscapes',
		'weapon',
		'new-year',
		'mood',
		'music',
		'men',
		'minimalism',
		'rendering',
		'situations',
		'dog',
		'sports',
		'style',
		'textures',
		'fantasy',
		'films',
		'flowers',
		'anime',
		'avto']
		
genre_anime = [
		'art-anime',
		'dzesey',
		'codomo',
		'other-anime',
		'sedze',
		'senen',
		'seinen']
		
genre_avto = [
		'alfa-romeo',
		'motorbike',
		'supercar',
		'other',
		'other-technics',
		'volvo',
		'volkswagen',
		'toyota',
		'suzuki',
		'subaru',
		'saab',
		'jaguar',
		'jeep',
		'kia',
		'lamborghini',
		'land-rover',
		'lexus',
		'maserati',
		'mazda',
		'mercedes',
		'mini',
		'mitsubishi',
		'nissan',
		'opel',
		'peugeot',
		'renault',
		'infiniti',
		'hyundai',
		'hummer',
		'honda',
		'ford',
		'ferrari',
		'dodge',
		'citroen',
		'chevrolet',
		'cadillac',
		'bugatti',
		'bmw',
		'bentley',
		'audi',
		'aston-martin']

time = ['day', 'week', '17day', 'month', 'all_time']
type = ['date', 'downloads', 'votings', 'comments', 'random']

class Config:
	genre = 'all'
	time = 'all_time'
	type = 'random'
	name = "wallpaper.jpg"
	is_blur = False
	resolution = "original" #1920x1080
	local_type = 'random'
	is_like = ""
		
def input_params():
	parser = argparse.ArgumentParser()
	parser.add_argument("-b", "--blur", action="store_true", default=False,
						help="add blur effect")
	parser.add_argument("--print_db", action="store_true", default=False,
						help="print tags and values")
	
	parser.add_argument("-g", "--genre", type=str, default='all',
						help="""set genre: 'all', 'hi-tech'," +
			'abstraction', 'aviation', 'city', 'girls', 'food', 'painting', 'animals',
			'games', 'space', 'interior', 'cats', 'macro', 'miscellanea', 'nature',
			'holidays', 'landscapes', 'weapon', 'new-year', 'mood', 'music', 'men',
			'minimalism', 'rendering', 'situations', 'dog', 'sports', 'style',
			'textures', 'fantasy', 'films', 'flowers', 
			'anime', ['art-anime', 'dzesey', 'codomo', 'other-anime', 'sedze', 'senen',
			'seinen']
			'avto', ['alfa-romeo', 'motorbike', 'supercar', 'other', 'other-technics',
			'volvo','volkswagen', 'toyota', 'suzuki', 'subaru', 'saab', 'jaguar', 'jeep',
			'kia', 'lamborghini', 'land-rover', 'lexus', 'maserati', 'mazda', 'mercedes',
			'mini', 'mitsubishi', 'nissan', 'opel', 'peugeot', 'renault', 'infiniti', 'hyundai',
			'hummer', 'honda', 'ford', 'ferrari', 'dodge', 'citroen', 'chevrolet', 'cadillac',
			'bugatti', 'bmw', 'bentley', 'audi', 'aston-martin']""")
			
	parser.add_argument("-t", "--time", type=str, default='all_time',
						help="image time period: 'day', 'week', '17day', 'month', 'all_time'")

	parser.add_argument("-r", "--resolution", type=str, default='original',
						help="image resolution WIDTHxHEIGHT \
							(if image do not have your resolution then download origin resolution)")
	parser.add_argument("-T", "--type", type=str, default='random',
					help="partition type: 'date', 'downloads', 'votings', 'comments', 'random'")
	
	parser.add_argument("-lt", "--local_type", type=str, default='random',
						help="partition type: 'first', 'random', 'max_votings'")
	
	parser.add_argument("-l", "--like", type=str, default='',
						help="like or dislike wallpaper: 'true', 'false'")
	
	parser.add_argument("-n", "--name", type=str, default='wallpaper.jpg',
						help="set filename")
	args = parser.parse_args()

	config.genre = args.genre
	config.time = args.time
	config.type = args.type
	config.name = args.name
	config.local_type = args.local_type
	config.resolution = args.resolution
	config.is_like = args.like
	
	if args.print_db:
		db.print_db()
		sys.exit()

def get_tags(url):
	wall_data = urllib.request.urlopen(url).read().decode('utf-8')
	find_keywords = re.compile('<span itemprop="description">' + '[a-zA-Z0-9/\-\\\.:<>=,\n\" `\'А-Яа-я_!"№;&\@#$%*\^%:?*()+]*' + '</span>')
	kw_data = ""
	for kw in find_keywords.finditer(wall_data):
		kw_data += kw.group()
	
	find_keywords = re.compile('>' + '[a-zA-Z0-9/\-\\:=\" `\'А-Яа-я_!"№;&\@#$%*\^%:?*()+]*' + '<')
	keywords = []
	for kw in find_keywords.finditer(kw_data):
		_kw = kw.group()
		keywords.append(_kw[1:len(_kw)-1].strip().lower())
	for kw in keywords:
		db.insert_and_get(kw, 0)
	return keywords

def get_max_valu_img(urls):
	wall_votings = []
	
	for url in urls:
		keywords = get_tags(url)
			
		#print(keywords)
		votings = 0
		for kw in keywords:
			res = db.insert_and_get(kw, 0)
			votings += res[1]
			#print(res[0], res[1])
		wall_votings.append(votings)
		
	#wall_votings.sort()
	#print(wall_votings)
	return wall_votings.index(max(wall_votings))
		
def load_image():
	_MAIN_URL = ""
	
	#url genre
	if not config.genre in genre+genre_anime+genre_avto:
		print("Error genre")
		sys.exit()
	if config.genre == 'all':
		_MAIN_URL = 'https://www.goodfon.ru/'
	elif config.genre == 'anime' or config.genre in genre_anime:
		if config.genre == 'anime':
			_MAIN_URL = 'https://anime.goodfon.ru/'
		else:
			_MAIN_URL = 'https://anime.goodfon.ru/catalog/' + config.genre + '/'
	elif config.genre == 'avto' or config.genre in genre_avto:
		if config.genre == 'avto':
			_MAIN_URL = 'https://avto.goodfon.ru/'
		else:
			_MAIN_URL = 'https://avto.goodfon.ru/catalog/' + config.genre + '/'
	else:
		_MAIN_URL = 'https://www.goodfon.ru/catalog/' + config.genre + '/'

	#type
	if not config.type in ['date', 'downloads', 'votings', 'comments', 'random']:
		print("Error type")
		sys.exit()
	if config.type == 'date':
		pass
	elif config.type == 'downloads':
		_MAIN_URL += 'downloads/'
	elif config.type == 'votings':
		_MAIN_URL += 'votings/'
	elif config.type == 'comments':
		_MAIN_URL += 'comments/'
	elif config.type == 'random':
		_MAIN_URL += 'random/'
	
	#time
	if not config.time in ['day', 'week', '17day', 'month', 'all_time']:
		print("Error time")
		sys.exit()
	if config.type == 'date' or config.time == 'all_time':
		pass
	elif config.time == 'day':
		_MAIN_URL += 'day/'
	elif config.time == 'week':
		_MAIN_URL += 'week/'
	elif config.time == '17day':
		_MAIN_URL += '17day/'
	elif config.time == 'month':
		_MAIN_URL += 'month/'
		
	print(_MAIN_URL)
	
	# get walls
	goodwalls = urllib.request.urlopen(_MAIN_URL).read().decode('utf-8')
	pos = 0
	image_urls = []
	if config.genre == 'anime' or config.genre in genre_anime:
		image_url_substring = 'https://anime.goodfon.ru/'
	elif config.genre == 'avto' or config.genre in genre_avto:
		image_url_substring = 'https://avto.goodfon.ru/'
	else:
		image_url_substring = "https://www.goodfon.ru/"
	
	#print(goodwalls)

	find_image = re.compile(image_url_substring + "[a-zA-Z0-9/-]*\.html")
	for im in find_image.finditer(goodwalls):
		image_urls.append(im.group())
		#print("Image url sub: ", im.group())
	if image_urls == []:
		print("Dont have wallpaper with this parameters")
		sys.exit()
	#local type
	if not config.local_type in ['first', 'random', 'max_votings']:
		print("Error local_type")
		sys.exit()
	if config.local_type == "first":
		wall_choice = 0
	elif config.local_type == "random":
		wall_choice = random.randint(0, len(image_urls)-1)
	else:
		wall_choice = get_max_valu_img(image_urls)
	
	#get images tags
	wall_tags = get_tags(image_urls[wall_choice])
	
	print("URL: ", image_urls[wall_choice])
	goodwalls = urllib.request.urlopen(image_urls[wall_choice]).read().decode('utf-8')
	
	pos = goodwalls.find("Скачать оригинал", 0)
	pos = goodwalls.find("href=", pos)
	result_image_url = ""
	i = 0
	if pos != -1:
		while goodwalls[pos + i] != '.':
			result_image_url += goodwalls[pos + i]
			i+=1
	else:
		print("Do not find image link")
		sys.exit(0)

	result_image_url += ".html"
	result_image_url = result_image_url[5:]
	#print(result_image_url)
	#sys.exit(0)
	#custom resolution TODO: delete it, easy resize by opencv or pillow
	if config.resolution == "original":
		pass
	else:
		find_resolution = re.compile('<option value="'+config.resolution+'">'+config.resolution+'</option>')
		fres = ""
		for kw in find_resolution.finditer(goodwalls):
			fres += kw.group()
		if fres != "":
			if result_image_url[len(result_image_url)-1] == "/":
				result_image_url = result_image_url[0:len(result_image_url)-1]
			while result_image_url[len(result_image_url)-1] != "/":
				result_image_url = result_image_url[0:len(result_image_url)-1]
			result_image_url += config.resolution + "/"
	
	if config.genre == 'anime' or config.genre in genre_anime:
		result_image_url = "https://anime.goodfon.ru" + result_image_url
	elif config.genre == 'avto' or config.genre in genre_avto:
		result_image_url = "https://avto.goodfon.ru" + result_image_url
	else:
		result_image_url = "https://www.goodfon.ru" + result_image_url
	#print("IMAGE: ", result_image_url)
	
	goodwalls = urllib.request.urlopen(result_image_url).read().decode('utf-8')
	pos = goodwalls.find('нажмите на картинку', 0)
	pos = goodwalls.find('https://', pos)
	
	result_image_url = ""
	i = 0
	if pos != -1:
		while goodwalls[pos + i] != '>':
			result_image_url += goodwalls[pos + i]
			i+=1
	else:
		print("Do not find image link")
		sys.exit(0)
	
	print("Image: ", result_image_url)
	res = urllib.request.urlopen(result_image_url).read()
	f = open(config.name, "wb")
	f.write(res)
	f.close()
	
	#blur
	if config.is_blur:
		img = Image.open(config.name)
		img = img.filter(ImageFilter.GaussianBlur(5))
		img.save(config.name, "JPEG")
	
	
	#save downloded image tags
	tags_list = []
	for t in wall_tags:
		_t = {
			'tag': t
		}
		tags_list.append(_t)

	
	outfile = open("cash.json", 'w')
	json.dump({'genre': config.genre, 'tags': tags_list}, outfile)
	
	
db = Database()
config = Config()
input_params()

if config.is_like != "":
	tags = []
	genre = ""
	try:
		f = open("cash.json", 'r')
	except IOError as e:
		pass
	else:
		data = f.read()
		js = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		genre = js.genre
		for e in js.tags:
			tags.append(e.tag)
	if config.is_like == "true":
		for t in tags:
			if t != genre:
				_t = db.select_tag(t)
				db.update_tag(_t[0], _t[1]+1)
	elif config.is_like == "false":
		for t in tags:
			if t != genre:
				_t = db.select_tag(t)
				db.update_tag(_t[0], _t[1]-1)
	sys.exit()

load_image()
