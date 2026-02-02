from mss import mss
import mss.tools
from numpy import asarray
from PIL import Image
from crop_icons import ICON_SIZE
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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
            ##icon_l = icon.convert("L")                                #converting to grayscale
            icon_l = icon_l.resize((ICON_SIZE*2, ICON_SIZE*2),Image.BICUBIC)                          
            ##icon_l = icon_l.point(lambda x: 0 if x < 140 else 255, "1")

            icon_arr = asarray(icon_l)                              #converting to numpy array
        
            return_arr_numpy.append(icon_arr)                             #appending to return array 
            return_arr_img.append(icon_l)                                 #appending to return array       
    return return_arr_numpy, return_arr_img
        

def difference(icon1, icon2):
    diff = 0
    for i in range(ICON_SIZE):
        for j in range(ICON_SIZE):
            diff += abs(int(icon1[i][j]) - int(icon2[i][j]))
    return diff



def find_lowest_diff(target_icon, icons_arr):
    lowest_diff = float('inf')
    for i in range(2):
        curent_diff = difference(target_icon, icons_arr[i])
        if curent_diff < lowest_diff:
            lowest_diff = curent_diff
    return lowest_diff



def get_stack(image):
    config = r"--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789"
    image = image.crop((0, ICON_SIZE, ICON_SIZE*2, ICON_SIZE*2))
    text = pytesseract.image_to_string(image, config=config)
    image.show()
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None




if __name__ == "__main__":
    ##img_strip = capture_strip() 
    img_strip = "sct-58x0_760x38.png"
    icons_numpy, icons_img = crop_icons(img_strip)
    
    stack_num = get_stack(icons_img[7])
    print(stack_num)


    

    