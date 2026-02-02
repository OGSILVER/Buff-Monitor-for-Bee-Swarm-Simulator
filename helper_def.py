from mss import mss
import mss.tools
from numpy import asarray
from PIL import Image
from crop_icons import ICON_SIZE
import pytesseract
import re






def difference(icon1, icon2):
    diff = 0
    icon1 = asarray(Image.open("BOOSTS/"+icon1))
    for i in range(ICON_SIZE):
        for j in range(ICON_SIZE):
            diff += abs(int(icon1[i][j]) - int(icon2[i][j]))
    return diff