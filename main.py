from classes import Buff
from concurrent.futures import as_completed, ThreadPoolExecutor
from helper_def import crop_icons,capture_strip


DIFF_POOL = ThreadPoolExecutor(max_workers=8)
OCR_POOL  = ThreadPoolExecutor(max_workers=4)
        


if __name__ == "__main__":
    looking_for = ["BLUE_BOOST"]
    buff_arr = []

    for buff_name in looking_for:
            buff_arr.append(Buff(buff_name))

    while True:
        numpy_arr, img_arr = crop_icons(capture_strip())
        active_buff_pool = []



        futures = []
        with DIFF_POOL as exec:
            futures = [exec.submit(buff.find_lowest_diff, numpy_arr) for buff in buff_arr]

            for f in as_completed(futures):
                try:
                    f.result()
                except Exception as e:
                    print(f"Error occurred: {e}")

        for buff in buff_arr:
            if buff.is_active:
                active_buff_pool.append(buff)

                
        with OCR_POOL as exec:
            futures = [exec.submit(buff.ocr_icon, img_arr[buff.icon_index]) for buff in active_buff_pool]
            
            for f in as_completed(futures):
                try:
                    f.result()
                except Exception as e:
                    print(f"Error occurred during OCR: {e}")
        
        for buff in active_buff_pool:
            if buff.name == "PRECISION" and not buff.is_being_checked:
                buff.precision_check(numpy_arr[buff.icon_index])

        wait = input("Press Enter to continue...")
        
    


    

    