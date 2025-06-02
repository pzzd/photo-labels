import PIL.Image
import PIL.ImageDraw
import face_recognition, os, shutil

source_dir = 'source'
source_list = os.listdir(source_dir)

output_dir = 'output/faces'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)


for file_name in source_list:

    if file_name == '.gitignore':
        continue

    file_name_prefix = file_name.split('.')[0]

    for index, (people_file_name) in enumerate(os.listdir('output/people-crops/' + file_name)):

        path = 'output/people-crops/' + file_name + '/' + people_file_name

        image = face_recognition.load_image_file(path)

        # Find all the faces in the image
        face_locations = face_recognition.face_locations(image)
        # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=4)

        number_of_faces = len(face_locations)
        print(f"{file_name} {people_file_name} : Detected {number_of_faces} face(s)")

        # Load the image into a Python Image Library object so that we can draw on top of it and display it
        pil_image = PIL.Image.fromarray(image)

        for face_location in face_locations:

            # Print the location of each face in this image. Each face is a list of co-ordinates in (top, right, bottom, left) order.
            top, right, bottom, left = face_location
            print(f"  At pixel location Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}")

            # Let's draw a box around the face
            # draw = PIL.ImageDraw.Draw(pil_image)
            # draw.rectangle([left, top, right, bottom], outline="red")

            cropped = pil_image.crop((left, top, right, bottom))

            this_output_dir = output_dir + "/" + file_name
            if not os.path.exists(this_output_dir):
                os.mkdir(this_output_dir)
            cropped.save(f"{this_output_dir}/{index}.jpg", 'JPEG')

        # Display the image on screen
        # pil_image.show()
