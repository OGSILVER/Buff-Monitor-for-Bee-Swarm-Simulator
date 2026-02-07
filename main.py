from classes import Buff
from concurrent.futures import as_completed, ThreadPoolExecutor
from helper_def import crop_icons,capture_strip
from PIL import Image
import time

DIFF_POOL = ThreadPoolExecutor(max_workers=4)
OCR_POOL  = ThreadPoolExecutor(max_workers=2)
        


if __name__ == "__main__":
    looking_for = ["MELODY", "FOCUS","BABY_LOVE","INSPIRE"]
    buff_arr = []

    for buff_name in looking_for:
            buff_arr.append(Buff(buff_name))

    while True:
        numpy_arr, img_arr = crop_icons(capture_strip())
        active_buff_pool = []



        futures = []
        futures = [DIFF_POOL.submit(buff.find_lowest_diff, numpy_arr) for buff in buff_arr]

        for f in as_completed(futures):
            try:
                print(f.result())
            except Exception as e:
                print(f"Error occurred: {e}")

        for buff in buff_arr:
            if buff.is_active:
                active_buff_pool.append(buff)


        futures = []                
        futures = [OCR_POOL.submit(buff.get_stack, img_arr[buff.icon_index]) for buff in active_buff_pool]
        
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                print(f"Error occurred during OCR: {e}")
        
        for buff in active_buff_pool:
            if buff.name == "PRECISION" and not buff.is_being_checked:
                buff.precision_check(numpy_arr[buff.icon_index])


        for buff in active_buff_pool:
            print(f"{buff.name} is {buff.is_active} with stack {buff.stack}")

##        wait = input("Press Enter to continue...")
##        time.sleep(1)
        
    


    

    