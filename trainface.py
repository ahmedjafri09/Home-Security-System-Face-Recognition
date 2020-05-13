import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import os
import sys
import mysql.connector as mariadb
from six.moves import input
from guizero import App, Text, TextBox, PushButton
from datetime import datetime

photoArray = []

mariadb_connection = mariadb.connect(user='samra', password='123456', database='securehome')
cursor = mariadb_connection.cursor()

name=""
def say_my_name():
    name = my_name.value
    app.destroy()
app = App(title="Train Face", width="300",height="150")
welcome_message = Text(app, text="Enter a Name")
my_name = TextBox(app)
update_text = PushButton(app, command=say_my_name, text="OK")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

app.display()
print(my_name.value)
dirName = "./images/" + my_name.value
print(dirName)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory Created")
else:
    print("Name already exists")
    sys.exit()

count = 1

now = datetime.now()
current= now.strftime("%m/%d/%Y, %H:%M:%S")
cursor.execute("""DELETE FROM camera WHERE Username=%s""",("samrakhalid00",))
cursor.execute("""INSERT INTO camera (Username,Time) VALUES (%s,%s)""",("samrakhalid00",current))
mariadb_connection.commit()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if count > 30:
        break
    frame = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    for (x, y, w, h) in faces:
        roiGray = gray[y:y+h, x:x+w]
        fileName = dirName + "/" + name + str(count) + ".jpg"
        cv2.imwrite(fileName, roiGray)
        photoArray.append(convertToBinaryData(fileName))
        cv2.imshow("face", roiGray)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        count += 1

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    rawCapture.truncate(0)

    if key == 27:
        break

cursor = mariadb_connection.cursor()
cursor.execute("""INSERT INTO Member (Name,Username,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (my_name.value, "samrakhalid00", photoArray[0],photoArray[1],photoArray[2],photoArray[3],photoArray[4],photoArray[5],photoArray[6],photoArray[7],photoArray[8],photoArray[9],photoArray[10],photoArray[11],photoArray[12],photoArray[13],photoArray[14],photoArray[15],photoArray[16],photoArray[17],photoArray[18],photoArray[19],photoArray[20],photoArray[21],photoArray[22],photoArray[23],photoArray[24],photoArray[25],photoArray[26],photoArray[27],photoArray[28],photoArray[29],))
mariadb_connection.commit()
cursor.close()
if (mariadb_connection.is_connected()):
    cursor.close()
    mariadb_connection.close()
    print("MySQL connection is closed")

os.system("python3 /home/pi/Documents/det_and_recog/trainrecognizer.py")

cv2.destroyAllWindows()
