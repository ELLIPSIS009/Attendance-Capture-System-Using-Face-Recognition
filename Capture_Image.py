import csv
import PySimpleGUI as sg
import cv2
import os

# counting the numbers
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

# Take image function
def takeImages():
    sg.theme('Black')
    layout = [[sg.Text('ID:', size =(7, 1), font='Helvetica 14'), sg.InputText('', font='Helvetica 14')],
              [sg.Text('Name:', size =(7, 1), font='Helvetica 14'), sg.InputText('', font='Helvetica 14')],
              [sg.Button('Submit', button_color=('white', '#303030'), font='Helvetica 14', size=(20,1)), 
              sg.Button('Cancel', button_color=('white', '#303030'), font='Helvetica 14', size=(20,1))]]
    window = sg.Window('Student Details', layout, element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            window.close()
            break
        elif event == 'Submit':
            Id = values[0]
            name = values[1]
            window.close()
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        sampleNum = 0
        layout = [ [sg.Text("Please look into the Camera",font='Helvetica 24')],
                   [sg.Text("Progress: "),sg.ProgressBar(101, orientation='h', size=(20, 20), key='progressbar')],
                   [sg.Image(filename='', key='image')],[sg.Button("Back to Menu",size=(40,1))] ]
        window = sg.Window('Capture Image', layout, auto_size_buttons=False, element_justification='c', location=(350, 75))
        progress_bar = window['progressbar']
        while(True):
            event, values = window.read(timeout=1)
            if event == "Back to Menu" or event == sg.WIN_CLOSED:
                cam.release()
                cv2.destroyAllWindows()
                window.close()
                break
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                #incrementing sample number
                sampleNum = sampleNum+1
                progress_bar.UpdateBar(int(sampleNum))
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage" + os.sep +name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                imgbytes = cv2.imencode(".png", img)[1].tobytes()
                window["image"].update(data=imgbytes)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        window.close()
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open("StudentDetails"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    else:
        takeImages()
