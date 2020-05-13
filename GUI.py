from guizero import App, Text, TextBox, PushButton
import tkinter as tk
import mysql.connector as mariadb
import os
from gpiozero import InputDevice
from gpiozero import OutputDevice
import time

pir = InputDevice(17)



def add():
    t["state"]="normal"
    b3["state"]="normal"
    
def enter():
    print("opening recognizer..")
    os.system("python3 /home/pi/Documents/det_and_recog/recognizeface.py")
def check():
    mariadb_connection = mariadb.connect(user='samra', password='123456', database='securehome')
    cursor = mariadb_connection.cursor()
    cursor.execute("""SELECT Password FROM User WHERE Username = %s""",("samrakhalid00",))
    record = cursor.fetchall()

    for row in record:
        p = row[0]
    if password.get()==p:
        print("matched")
        print("opening trainer..")
        t.delete(0,"end")
        t["state"]= "disabled"
        b3["state"]= "disabled"
        os.system("python3 /home/pi/Documents/det_and_recog/trainface.py")
    else:
        print("incorrect password")
        
        
master = tk.Tk()
master.title("Face recognition")
master.geometry("300x250")
b1 = tk.Button(master, text="Select if you are a member",height="2", font="6px"  , width="24", bg='deep sky blue', command = enter)
b2 = tk.Button(master, text="Select if you are new",height="2", font="6px"  , width="24", bg='deep sky blue', command = add)
b3 = tk.Button(master, text="Ok",height="2",font="6px" , width="12", bg='deep sky blue', command = check)
l = tk.Label(master,text="Enter Password",font="6px")
password = tk.StringVar()
t = tk.Entry(master, textvariable=password, show='*', width="36")

b1.pack()
b2.pack()
l.pack()
t["state"]= "disabled"
t.pack()
b3["state"]= "disabled"
b3.pack(padx=15,pady=5, side="right")
count = 0
while True:
    if pir.value == 0:
        count = count+1
        if count>=10000:
            master.destroy()
    
    master.update()
    
