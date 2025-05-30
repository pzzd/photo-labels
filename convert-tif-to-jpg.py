from PIL import Image
import os
import shutil

Image.MAX_IMAGE_PIXELS = 900000000

output_dir = 'output/jpgs'
# TODO: save that .gitgnore
os.mkdir(output_dir)

source_dir = 'source'
source_list = os.listdir(source_dir)
print(source_list)

for file_name in source_list:

    if file_name == '.gitignore':
        continue

    file_name_prefix = file_name.split('.')[0]

    this_output_dir = output_dir + "/" + file_name
    os.mkdir(this_output_dir)

    tiff_image = Image.open(source_dir + "/" + file_name)
    jpeg_image = tiff_image.convert("RGB")
    jpeg_image.save(this_output_dir+'/' + file_name_prefix + '.jpg', 'JPEG')