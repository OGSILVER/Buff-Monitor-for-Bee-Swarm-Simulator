from numpy import asarray
from PIL import Image
from SSIM_PIL import compare_ssim as ssim

from crop_icons import ICON_SIZE


image1 = Image.open("BOOSTS/FOCUS.png")
image2 = Image.open("focus1.png")
image2 = image2.convert("L")                                

image1 = image1.crop((0, 0, ICON_SIZE, ICON_SIZE//2+4))
image2 = image2.crop((0, 0, ICON_SIZE, ICON_SIZE//2+4))
image1.save("img1_crop.png")
image2.save("img2_crop.png")

value = ssim(image2, image1)

print(value)