import os, shutil, base64, json
from ollama import chat
from ollama import ChatResponse
from ollama import generate
from PIL import Image


Image.MAX_IMAGE_PIXELS = 900000000

output_dir = 'output/metadata'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)

source_dir = 'source'
source_list = os.listdir(source_dir)

for file_name in source_list:

    if file_name == '.gitignore':
        continue

    file_name_prefix = file_name.split('.')[0]

    # this_output_dir = output_dir + "/" + file_name
    # os.mkdir(this_output_dir)

    image_path = "output/jpgs/" + file_name +"/" + file_name_prefix + ".jpg"

    with open(image_path, 'rb') as imgfile:
        base64_bytes = base64.b64encode(imgfile.read())
        base64_encoded = base64_bytes.decode()

        # print ('GENERATE '+file_name)
        # x = generate(model='llava:13b', prompt='What is in this picture?', images=[base64_encoded], think='yes')
        # print (x)

        # print ('CHAT '+file_name)
        response: ChatResponse = chat(model='llava:13b', messages=[
            {
                'role': 'user',
                'content': 'What is in this picture?',
                'images': [base64_encoded],
                'think': 'yes'
            },
        ])
        # print(response.message.content)
        # print ('---')


        number_of_people = len(os.listdir("output/people-crops/"+file_name))

        # Data to be written
        dictionary = {
            "description": response.message.content,
            "number_of_people": number_of_people
        }

        with open("output/metadata/"+file_name+".json", "w") as outfile:
            json.dump(dictionary, outfile)