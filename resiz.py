import PIL
import os
from PIL import Image
from os import listdir
from os.path import isfile, join
import sys


def list_fils():
    pth = './'
    return [f for f in listdir(pth) if isfile(join(pth, f))]


def convierte(baseh=300.0):
    pics = [f for f in list_fils() if not f.endswith('.py')]
    for p in pics:
        img = Image.open(p)
        height = int(baseh)
        width = int((baseh / img.size[1]) * img.size[0])
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        img.save(os.path.join('./Resiz/', p))


if __name__ == '__main__':
    convierte(*[float(x) for x in sys.argv[1:]])
