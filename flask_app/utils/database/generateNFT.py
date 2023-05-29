import os
import random
from PIL import Image

# generate a random jpg file and return its path
def generateRandomJPG():
    # generate a random and not exist filename
    while True:
        filename = f"flask_app/static/nft/images/{random.randint(1, 1000000)}.jpg"
        if not os.path.exists(filename):
            break

    # create a new image with random colors
    image = Image.new('RGB', (100, 100), color='black')
    pixels = image.load()
    for x in range(100):
        for y in range(100):
            pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    image.save(filename, format= 'JPEG')
    return filename
