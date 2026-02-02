from mss import mss
import mss.tools
from numpy import asarray
from PIL import Image
from crop_icons import ICON_SIZE
import pytesseract
import re
from classes import Buff

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


from concurrent.futures import ThreadPoolExecutor

DIFF_POOL = ThreadPoolExecutor(max_workers=8)
OCR_POOL  = ThreadPoolExecutor(max_workers=4)

def capture_strip():
    
    with mss.mss() as sct:
        
        monitor = {"top": 58, "left": 0, "width": 760, "height": ICON_SIZE}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        sct_img = sct.grab(monitor)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output = output)
        return output



def crop_icons(output):
    with Image.open(output) as img:
        return_arr_numpy = []
        return_arr_img = []
        for i in range(20):
            left = i * ICON_SIZE
            top = 0
            right = left + ICON_SIZE
            bottom = ICON_SIZE

            icon_l = img.crop((left, top, right, bottom))             #cropping the icon
            icon_l = icon_l.convert("L")                                #converting to grayscale
                        
            ##icon_l = icon_l.point(lambda x: 0 if x < 140 else 255, "1")

            icon_arr = asarray(icon_l)                              #converting to numpy array
        
            return_arr_numpy.append(icon_arr)                             #appending to return array 
            return_arr_img.append(icon_l)                                 #appending to return array       
    return return_arr_numpy, return_arr_img
        


if __name__ == "__main__":
    looking_for = ["BLUE_BOOST"]
    buff_arr= []
    active_buff_pool = []

    for buff_name in looking_for:
            buff_arr.append(Buff(buff_name))

    while True:
        numpy_arr, img_arr = crop_icons(capture_strip())
        for buff in buff_arr:
            buff.find_lowest_diff(numpy_arr)


        for buff in buff_arr:
            if buff.is_active:
                active_buff_pool.append(buff)

                
        for buff in active_buff_pool:
            buff.get_stack(img_arr[buff.icon_index])
        


        wait = input("Press Enter to continue...")
        
    


    

    