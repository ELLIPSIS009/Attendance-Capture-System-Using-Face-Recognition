import os
import cv2
import numpy as np
from PIL import Image
import PySimpleGUI as sg

# image labesl
def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    value = len(imagePaths)
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    i = 1
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
        sg.one_line_progress_meter('Image Training Model', i, value, 'key', 'Training Time Left: ',orientation="h")
        i+=1
    return faces, Ids

# train images function
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces, Id = getImagesAndLabels("TrainingImage")
    target = recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel"+os.sep+"Trainner.yml")
    sg.popup_auto_close('All Images Trained')
