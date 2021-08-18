import face_recognition
import cv2
import os
import numpy as np

data_dict={}
path="Dataset/"
for persons in os.listdir(path):
    pname = path + persons
    for images in os.listdir(pname):
        image_path = pname + '/' + images
        name=persons.split("_")[0]
        idx = persons.split("_")[1]
        image = cv2.imread(image_path)
        print(image.shape)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(image, boxes)
        for encoding in encodings:
            data_dict[str(name)]=data_dict.get(name,[idx, encoding])
            np.save("embeddings_face.npy",data_dict)
