from PIL import Image
from PIL import UnidentifiedImageError
import os

# input picture to be compressed, and the wanted quality, it will overwrite existing image
def compress(jpg, new_quality):
    image = Image.open(jpg)
    width, height = image.size
    new_size = (width//4, height//4)
    resized_image = image.resize(new_size)
    resized_image.save(jpg, optimize=True, quality=new_quality)
    print(jpg+" Has been optimized with the chosen quality")

# Function to walk through nested folder, and give them as input to compress()
def list_files(dir):
#    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            try:
                print(root+"/"+name)
                
                #compress(root+"/"+name, 70)
            except UnidentifiedImageError:
                print(root+"/"+name+" Is not working with Pillow")
                continue
#    return r

# compress("pic/Border82-2.jpg", 70)
list_files("pic")