import os
import sys
from random import randint
from sty import fg
from PIL import Image
from numpy import asarray

os.system("")
file = sys.argv[1]
image = Image.open(file)
width, height = image.size
new_width = 119
new_size = (new_width, int((height * new_width) / (width * 2)))
img = image.resize(new_size, Image.ANTIALIAS)

data = asarray(img)
for i in data:
	for j in i:
		char = str(randint(0,9))
		pix = fg(j[0], j[1], j[2]) + char
		print(pix, end='')
	print('', end='\n')
input()