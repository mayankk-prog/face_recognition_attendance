import cv2
import face_recognition
import pickle
import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecog-cfdcc-default-rtdb.firebaseio.com/',
    'storageBucket': 'facerecog-cfdcc.appspot.com'
})

folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    filename= f'{folderPath}/{path}'
    bucket= storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

print(studentIds)


def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open('Encodefile.p', 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
