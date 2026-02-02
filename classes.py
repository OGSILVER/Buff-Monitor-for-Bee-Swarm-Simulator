BUFF_DURATIONS = {
    "BLUE_BOOST":15,
    "RED_BOOST":15,
    "WHITE_BOOST":15,
    "FOCUS":20,
    "MELODY":30,
    "BABY_LOVE":30,
    "BEAR_MORPH":30,
    "INSPIRE":5,
    "PRECISION":60,
    "PRECISE_MARK":None,
    "FLAME_HEAT":None,
    "SCORCHING_STAR":45,
    "SUPER_SMOOTHIE":20*60,

}

PRECISION_FULL_COLOR = 109

from mss import mss
import mss.tools
from numpy import asarray
from PIL import Image
from crop_icons import ICON_SIZE
import pytesseract
import re
import time
import math


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


from helper_def import  difference

class Buff:
    spaces = list(range(1,21))
    def __init__(self, name, duration= None, icon_index=None, stack=0, is_active=False):
        self.name = name
        self.duration = BUFF_DURATIONS[name]
    

    def find_lowest_diff(self, icons_arr):
        lowest_diff = float('inf')
        for image in icons_arr:
            curent_diff = difference(self.name+".png", image)
            if curent_diff < lowest_diff:
                lowest_diff = curent_diff
                lowest_diff_image = image
                
        self.icon_index = icons_arr.index(lowest_diff_image)
        if lowest_diff < 3000:
            self.is_active = True
    

    def get_stack(self, image):
        config = r"--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789"
        image = image.resize((ICON_SIZE*2, ICON_SIZE*2),Image.BICUBIC) 
        image = image.crop((0, ICON_SIZE, ICON_SIZE*2, ICON_SIZE*2))
        text = pytesseract.image_to_string(image, config=config)
        match = re.search(r"\d+", text)
        
        self.stack = int(match.group()) if match else None

    def check_status(self, image):
        if self.name == "PRECISION":
            color_full = PRECISION_FULL_COLOR

            if image[30][1] != color_full:
                ##make a warning sound here
                time.sleep(math.floor(self.duration*0.2))
                if image[30][1] != color_full:
                    self.is_active = False
            
        
    
        