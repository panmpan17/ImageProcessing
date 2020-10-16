from color import *
from PIL import Image
from utilities import ProgressBar


def decimal_2_binary(n):
    if n > 1:
        return decimal_2_binary(n // 2) + str(n % 2)
    return str(n % 2)


img = Image.open("test.JPG")

seperate = []
for i in range(8):
    seperate.append(Image.new("RGB", (img.width, img.height)))

progress_bar = ProgressBar(img.width * img.height,
                           "Progress: ", "Completed", length=50)

for x in range(img.width):
    for y in range(img.height):
        rgb = RGBColor(*img.getpixel((x, y)))
        hsv = rgb.to_HSV()

        binary = decimal_2_binary(int(hsv.V * 255))
        if len(binary) < 8:
            binary = "0" * (8 - len(binary)) + binary

        for i, _img in enumerate(seperate):
            if binary[i] == "1":
                _img.putpixel((x, y), WHITE.tuple)  # WHITE
            else:
                _img.putpixel((x, y), BLACK.tuple)
        
        progress_bar.increment()

for i, _img in enumerate(seperate):
    _img.save(f"test-{i}.png")
    _img.close()

img.close()
