#!/usr/bin/env python
from tokenize import String
import PySimpleGUI as sg
import cv2
import numpy as np
# importing os module  
import os

"""
Demo program that displays a webcam using OpenCV
"""
def detect_face(img, gray_image, original_image, face_cascade, height,width):
    # print(width,height)
    detected_faces = face_cascade.detectMultiScale(
        image=gray_image, scaleFactor=1.3, minNeighbors=8)
    face = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    for (x, y, w, h) in detected_faces:
        cv2.rectangle(original_image, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)

        width_ratio = w/width
        height_ratio = (h/height)


        y_dist = min(y, height-y, 0.25*(height))
        x_dist = min(x, width-x *width_ratio, 0.25*(width))

        max_width = (w*3)*width_ratio
        side = (max_width-w)/2
        
        right = int(x_dist)+side+w
        left = int(x_dist) + side
        
        if x < w:
            right += (w-x)

        if (width-x) < w:
            left += (w+x)

        face = img[y - int(y_dist):y + int(y_dist)+h , x-int(left):x+int(right)]
    resize = cv2.resize(face,(800,600))
    return resize

def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Follow Face Filter', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Capture', size=(10, 1), font='Any 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('CMSC 174 - Final Project - Follow Face',
                       layout, location=(900, 600))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = False
    width  = cap.get(3)
    height = cap.get(4)

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Start':
            recording = True
        
        elif event == 'Capture' and recording:
            cv2.imwrite("hello.jpg", frame)
            path = os.getcwd()+"\hello.jpg"
            os.system(path)


        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        if recording:
            ret, img = cap.read()
            original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            frame = detect_face(img, gray_image, original_image, face_cascade, height,width)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)


main()