import face_recognition, json, os

source_dir = 'source/known-faces'
source_list = os.listdir(source_dir)

for file_name in source_list:

    file_name_prefix = file_name.split('.')[0]

    image = face_recognition.load_image_file(os.path.join(source_dir, file_name))
    face_encoding = face_recognition.face_encodings(image)[0]

# TODO: TypeError: Object of type ndarray is not JSON serializable
    dictionary = {
        "file_name": file_name,
        "encoding": face_encoding
    }

    with open("source/known-faces-encoded/"+file_name_prefix+".json", "w") as outfile:
       json.dump(dictionary, outfile)

