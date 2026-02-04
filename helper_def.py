from mss import mss
import mss.tools
from numpy import asarray
from PIL import Image
from crop_icons import ICON_SIZE




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




def difference(icon1, icon2):
    diff = 0
    icon1 = asarray(Image.open("BOOSTS/"+icon1))
    for i in range(ICON_SIZE):
        for j in range(ICON_SIZE):
            diff += abs(int(icon1[i][j]) - int(icon2[i][j]))
    return diff