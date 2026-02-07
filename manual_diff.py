from numpy import asarray
from PIL import Image

from crop_icons import ICON_SIZE



for i in range(1,19):
    diff = 0
    icon1 = asarray(Image.open("BOOSTS/FOCUS.png"))
    icon2 = asarray(Image.open(f"block{i}.png"))
    for i in range(ICON_SIZE):
        for j in range(ICON_SIZE):
            diff += abs(int(icon1[i][j]) - int(icon2[i][j]))


    print(str(diff) + " on image" + str(i))