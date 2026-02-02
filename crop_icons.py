from mss import mss
import mss.tools
from numpy import asarray

from PIL import Image

ICON_SIZE = 38


def capture_strip():
    with mss.mss() as sct:
    
        monitor = {"top": 58, "left": 0, "width": 760, "height": ICON_SIZE}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        sct_img = sct.grab(monitor)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output = output)
        return output


def crop_icons(output):   #and save each icon as image
    with Image.open(output) as img:
        return_arr = []
        for i in range(20):
            if i > 2:
                left = i * ICON_SIZE
                top = 0
                right = left + ICON_SIZE
                bottom = ICON_SIZE
    
                icon = img.crop((left, top, right, bottom))             #cropping the icon
                icon_l = icon.convert("L")
                icon_l.save(f"block{i}.png")                              #converting to grayscale


                 
if __name__ == "__main__":
    crop_icons(capture_strip())
    print("yo i entered this file lol") 