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

from numpy import asarray
from PIL import Image
from crop_icons import ICON_SIZE
import pytesseract
import re
import time
import math
import threading


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
##pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract-ocr"



from helper_def import  difference

class Buff:
    def __init__(self, name):
        self.name = name
        self.duration = BUFF_DURATIONS[name]

        # internal state (set/updated by checks later)
        self.icon_index = None
        self.stack = 0
        self.is_active = False
        self.is_being_checked = False
        self.is_max_stack = False
        self._bg_thread = None
        self.diff = float('inf')

    def find_lowest_diff(self, icons_arr):
        lowest_diff = float('inf')
        lowest_diff_index = None
        for i,image in enumerate(icons_arr):
            curent_diff = difference(self.name+".png", image)
            if curent_diff < lowest_diff:
                lowest_diff = curent_diff
                lowest_diff_index = i

                
  
        if lowest_diff < 70000:
            self.is_active = True
            self.icon_index = lowest_diff_index
        else:
            self.is_active = False
            self.icon_index = None

        
        return lowest_diff, self.name

    def get_stack(self, image):
        config = r"--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789"
        image = image.resize((ICON_SIZE*2, ICON_SIZE*2),Image.BICUBIC) 
        image = image.crop((0, ICON_SIZE, ICON_SIZE*2, ICON_SIZE*2))
        text = pytesseract.image_to_string(image, config=config)
        match = re.search(r"\d+", text)
        
        self.stack = int(match.group()) if match else None

    def precision_check(self, image):

        def check_status():

            while self.is_being_checked:
                if self.stack != 10:
                    self.is_max_stack = False
                else:
                    self.is_max_stack = True
                
                color_full = PRECISION_FULL_COLOR

                if image[30][1] != color_full:
                        ##make a warning sound here and status is running out
                    time.sleep(math.floor(self.duration*0.25))
                    if image[30][1] != color_full:
                        self.is_active = False
                        self.is_being_checked = False
                
                time.sleep(1)
            
        if self._bg_thread is None or not self._bg_thread.is_alive():
            self._bg_thread = threading.Thread(target=check_status, daemon = True)
            self.is_being_checked = True
            self._bg_thread.start()

        
            
        
    
        