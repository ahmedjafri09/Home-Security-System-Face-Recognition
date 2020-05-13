import os
import numpy as np 
from PIL import Image 
import cv2
import pickle
import mysql.connector as mariadb

photoArray = []

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

mariadb_connection = mariadb.connect(user='samra', password='123456', database='securehome')
cursor = mariadb_connection.cursor()

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir, "images")

currentId = 1
labelIds = {}
yLabels = []
xTrain = []

cursor.execute("""SELECT * FROM Member WHERE Username=%s""",("samrakhalid00",))
record = cursor.fetchall()

for row in record:
    print("Id = ", row[1], )
    print("Name = ", row[0])
    label=row[0]
    if not label in labelIds:
        labelIds[label] = currentId
        print(labelIds)
        currentId += 1
        for x in range(30):     
            image = row[x+2]
            id_ = labelIds[label]
            write_file(image, "/home/pi/Documents/det_and_recog/images/photo.jpg")
            pilImage = Image.open("/home/pi/Documents/det_and_recog/images/photo.jpg").convert("L")
            imageArray = np.array(pilImage, "uint8")
            faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = imageArray[y:y+h, x:x+w]
                xTrain.append(roi)
                yLabels.append(id_)
        os.remove("/home/pi/Documents/det_and_recog/images/photo.jpg")
            
with open("labels", "wb") as f:
    pickle.dump(labelIds, f)
    f.close()

recognizer.train(xTrain, np.array(yLabels))
recognizer.save("trainer.yml")

cursor.execute("""DELETE FROM Train WHERE Username=%s""",("samrakhalid00",))
cursor.execute("""INSERT INTO Train (Username,YML,Label) VALUES (%s,%s,%s)""",("samrakhalid00",convertToBinaryData("/home/pi/Documents/det_and_recog/trainer.yml"),convertToBinaryData("/home/pi/Documents/det_and_recog/labels")))
mariadb_connection.commit()
cursor.close()
print(labelIds)
mariadb_connection.close()
os.remove("labels")
os.remove("trainer.yml")