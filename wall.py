import urllib.request
import random
import sys
import re
from PIL import Image
from PIL import ImageFilter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--blur", action="store_true",
                    help="add blur effect")
parser.add_argument("-g", "--genre", action="append",
                    help="set genre: 'hi-tech'," +
		"'abstraction', 'aviation', 'city', 'girls', 'food', 'painting', 'animals'," +
        "'games', 'space', 'interior', 'cats', 'macro', 'miscellanea', 'nature'," +
		"'holidays', 'landscapes', 'weapon', 'new-year', 'mood', 'music', 'men'," +
        "'minimalism', 'rendering', 'situations', 'dog', 'sports', 'style'," +
        "'textures', 'fantasy', 'films', 'flowers', 'anime', 'avto'")
parser.add_argument("-t", "--time", action="append",
                    help="image time: 'day', 'week', '17day', 'month'")
parser.add_argument("-n", "--name", action="append",
                    help="set filename")
args = parser.parse_args()

genre = ['hi-tech',
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
         'avto'
         ]

time = ['day', 'week', '17day', 'month']

_GANRE = 'all'
_TIME = ''
WALL_NAME = "wallpaper.jpg"

if args.genre != None and genre.count(args.genre[0]) != 0:
    _GANRE = args.genre[0]
if args.time != None and time.count(args.time[0]) != 0:
    _TIME = args.time[0]
if args.name != None:
    WALL_NAME = args.name[0]

_MAIN_URL = ""
if _GANRE == 'all':
    _MAIN_URL = 'https://www.goodfon.ru/random/' + _TIME + '/'
elif _GANRE == 'anime':
    _MAIN_URL = 'https://anime.goodfon.ru/random/' + _TIME + '/'
elif _GANRE == 'avto':
    _MAIN_URL = 'https://avto.goodfon.ru/random/' + _TIME + '/'
else:
    _MAIN_URL = 'https://www.goodfon.ru/catalog/' + _GANRE + '/random/' + _TIME + '/'
    
goodwalls = urllib.request.urlopen(_MAIN_URL).read().decode('utf-8')

pos = 0
imSrc = []
imSubStr = ''
if _GANRE == 'anime':
    imSubStr = 'https://anime.goodfon.ru/'
elif _GANRE == 'avto':
    imSubStr = 'https://avto.goodfon.ru/'
else:
    imSubStr = "https://www.goodfon.ru/wallpaper/"

p = re.compile(imSubStr + "[a-zA-Z0-9/-]*\.html")
for m in p.finditer(goodwalls):
	imSrc.append(m.group())
wallChoice = random.randint(0, len(imSrc)-1)

goodwalls = urllib.request.urlopen(imSrc[wallChoice]).read().decode('utf-8')
pos = goodwalls.find("Скачать оригинал:", 0)
pos = goodwalls.find("/download/", pos)
im = ""
i = 0
if pos != -1:
    while goodwalls[pos + i] != '"':
        im += goodwalls[pos + i]
        i+=1
else:
    sys.exit(0)

if _GANRE == 'anime':
    im = "https://anime.goodfon.ru" + im
elif _GANRE == 'avto':
    im = "https://avto.goodfon.ru" + im
else:
    im = "https://www.goodfon.ru" + im

goodwalls = urllib.request.urlopen(im).read().decode('utf-8')

pos = goodwalls.find('нажмите на картинку', 0)

pos = goodwalls.find('https://', pos)

im = ""
i = 0
if pos != -1:
    while goodwalls[pos + i] != '"':
        im += goodwalls[pos + i]
        i+=1
else:
    sys.exit(0)

res = urllib.request.urlopen(im).read()
f = open(WALL_NAME, "wb")
f.write(res)
f.close()
if args.blur:
    img = Image.open(WALL_NAME)
    img = img.filter(ImageFilter.GaussianBlur(5))#BoxBlur
    img.save(WALL_NAME, "JPEG")
