import os
import pickle
from datetime import datetime

import cv2
import cvzone
import face_recognition
import numpy as np


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecog-cfdcc-default-rtdb.firebaseio.com/',
    'storageBucket': 'facerecog-cfdcc.appspot.com'
})

bucket = storage.bucket()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/MODES'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

file = open('Encodefile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)

modeType=0
counter= 0
id=-1
imgStudent= []

while True:
    success, img = cap.read()

    imgS= cv2.resize(img,(0,0),None,0.25,0.25)
    imgS= cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurrFrame= face_recognition.face_locations(imgS)
    encodeCurFrame= face_recognition.face_encodings(imgS,faceCurrFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurrFrame):
            matches=face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches ",matches)
            # print("faceDis", faceDis)

            matchIndex= np.argmin(faceDis)
            # print("matchIndex", matchIndex)

            if matches[matchIndex]:
                # print(studentIds[matchIndex])
                y1,x2,y2,x1=faceLoc
                y1, x2, y2, x1= y1*4,x2*4,y2*4,x1*4
                bbox= 250+x1, 55+y1, x2-x1, y2-y1
                imgBackground=cvzone.cornerRect(imgBackground, bbox, rt=0)
                id= studentIds[matchIndex]
                print(id)
                if counter == 0:
                    counter= 1
                    modeType=1
        if counter!=0:
            if counter==1:
                studentInfo= db.reference(f'Students/{id}').get()
                print(studentInfo)
                blob= bucket.blob(f'Images/{id}.jpg')
                array= np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    print("Face detected at coordinates: (x={}, y={}, w={}, h={})".format(int(x), int(y), int(w), int(h)))
                studentInfo['x'] = int(x)  # Convert x coordinate to int
                studentInfo['y'] = int(y)  # Convert y coordinate to int
                studentInfo['w'] = int(w)  # Convert width to int
                studentInfo['h'] = int(h)  # Convert height to int

                # Update the 'x', 'y', 'w', and 'h' values in the Firebase database
                ref = db.reference(f'Students/{id}')
                ref.update({
                    "x": studentInfo['x'],
                    "y": studentInfo['y'],
                    "w": studentInfo['w'],
                    "h": studentInfo['h']
                })

                datetimeobject= datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                secondsElapsed=(datetime.now()-datetimeobject).total_seconds()
                print(secondsElapsed)

                if secondsElapsed>30:
                    ref= db.reference(f'Students/{id}')
                    studentInfo['total_attendance']+=1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType=3
                    counter=0
                    imgBackground[44:44+633, 808:808+414]= imgModeList[modeType]

            if modeType!=3:

                if 10<counter<20:
                    modeType=2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter<=10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']),(900,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (97 ,97,97), 1)
                    cv2.putText(imgBackground, str(studentInfo['name']),(950,505), cv2.FONT_HERSHEY_SIMPLEX, 1, (97,97,97), 1)
                    cv2.putText(imgBackground, str(studentInfo['id']),(900,575), cv2.FONT_HERSHEY_SIMPLEX, 1, (97,97,97), 1)

                    imgBackground[175:175+216, 909:909+216] = imgStudent

                counter= counter+1

                if counter>=20:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    imgStudent=[]
                    imgBackground[44:44+633, 808:808+414]= imgModeList[modeType]
    else:
        modeType=0
        counter=0
    cv2.imshow('webCam', img)
    cv2.imshow('attendance', imgBackground)
    cv2.waitKey(1)
