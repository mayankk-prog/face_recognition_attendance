from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecog-cfdcc-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')
data = {
    "123":
        {
            "name": "Mayank",
            "age": 19,
            "id": 123,
            "gender": "Male",
            "total_attendance": 23,
            "last_attendance_time": "2024-04-24 00:00:00",
            "x": 1,
            "y": 1,
            "w": 1,
            "h": 1
        },
    "456":
        {
            "name": "ujjawal",
            "age": 20,
            "id": 456,
            "gender": "Male",
            "total_attendance": 0,
            "last_attendace_time": "2024-04-24 00:00:00",
            "x": 1,
            "y": 1,
            "w": 1,
            "h": 1
        }
}

for key, value in data.items():
    ref.child(key).set(value)
