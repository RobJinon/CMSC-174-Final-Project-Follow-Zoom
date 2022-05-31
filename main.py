import cv2
import numpy as np
import PySimpleGUI as sg


def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Follow Face Filter', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]


    # create the window and show it without the plot
    window = sg.Window('CMSC 174 - Final Project - Follow Face',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    open = False

    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'Start':
            open = True


        if open:
            cam = cv2.VideoCapture(0)
            width  = cam.get(3)
            height = cam.get(4)

            while True:
                _, img = cam.read(0)
                img = cv2.flip(img, 1)

                original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # loading the classifier
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

                # face detection
                def detect_face(gray_image, original_image, face_cascade):
                    detected_faces = face_cascade.detectMultiScale(
                        image=gray_image, scaleFactor=1.3, minNeighbors=8)
                    for (x, y, w, h) in detected_faces:
                        cv2.rectangle(original_image, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)

                        face = img[y:y + h, x:x + w]
                        cv2.imshow("cropped face", face)
                        
                    return cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)

                # displaying the results
                cv2.namedWindow('Cam', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Cam', int(width), int(height))
                cv2.namedWindow('cropped face', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('cropped face', int(height/2), int(height/2))
                image_with_detections = detect_face(gray_image, original_image, face_cascade)
                cv2.imshow("Cam", image_with_detections)
                k = cv2.waitKey(30)
                if k == 27:
                    break
            cv2.destroyAllWindows()
            open = False
            


main()
