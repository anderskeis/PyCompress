# Remember to install the Pillow library first "pip install pillow"
from PIL import Image
from PIL import UnidentifiedImageError
import os

#Set Quality 1-100
chosen_quality = 70
#Size of picture
resize_divide_by = 2

#Starting directory where your files are located
path_to_pictures = "pic"

# input picture to be compressed, and the wanted quality, it will overwrite existing image!
def compress(jpg, new_quality):
    image = Image.open(jpg)
    width, height = image.size
    new_size = (width//resize_divide_by, height//resize_divide_by)
    resized_image = image.resize(new_size)
    resized_image.save(jpg, optimize=True, quality=new_quality)
    print(jpg+" Has been optimized with the chosen quality")

# Function to walk through nested folder, and give them as input to compress()
def compress_files(dir):

    for root, dirs, files in os.walk(dir):
        for name in files:
            try:
                print(root+"/"+name)
                
                compress(root+"/"+name, chosen_quality)
            except UnidentifiedImageError:
                print(root+"/"+name+" Is not working with Pillow")
                continue


# 
compress_files("pic")