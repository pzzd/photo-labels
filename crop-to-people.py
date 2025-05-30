from transformers import AutoImageProcessor, ConditionalDetrForObjectDetection
import torch
from PIL import Image
import PIL.ImageDraw
import requests
import numpy as np
import shutil
import os

Image.MAX_IMAGE_PIXELS = 900000000

source_dir = 'source'
source_list = os.listdir(source_dir)

output_dir = 'output/people-crops'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)

for file_name in source_list:

    if file_name == '.gitignore':
        continue

    file_name_prefix = file_name.split('.')[0]
    path = 'output/jpgs/' + file_name + '/' + file_name_prefix + '.jpg'

    image = Image.open(path)

    # print ("Original image shape: ")
    # print(np.array(image).shape)

    processor = AutoImageProcessor.from_pretrained("microsoft/conditional-detr-resnet-50")
    model = ConditionalDetrForObjectDetection.from_pretrained("microsoft/conditional-detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.7
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.7)[0]

    for index, (score, label, box) in enumerate(zip(results["scores"], results["labels"], results["boxes"])):
        box = [round(i, 2) for i in box.tolist()]
        print(
                f"{file_name} {index}: Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
        )

        # x0, y0, x1, y1
        left, top, right, bottom = box

        cropped = image.crop((left, top, right, bottom))

        this_output_dir = output_dir + "/" + file_name
        if not os.path.exists(this_output_dir):
            os.mkdir(this_output_dir)
        cropped.save(f"{this_output_dir}/{index}.jpg", 'JPEG')
