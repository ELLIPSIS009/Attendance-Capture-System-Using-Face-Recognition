import datetime
import os
import time
import PySimpleGUI as sg
import cv2
import pandas as pd

def recognize_attendence():
    sg.theme('Black')
    layout = [  [sg.Image(filename='', key='image'),
                [sg.Text(f'Date : {datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")}', key='_date_', font=('Helvetica 18'))], 
                [sg.Text(f'Time : {datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")}', key='_time_', font=('Helvetica 18'))]],
                [sg.Button("Clock IN",size=(25,2), font=('Helvetica 13'), button_color=('white', '#303030')),sg.Button("Clock OUT",size=(25,2), font=('Helvetica 13'), button_color=('white', '#303030')), sg.Button("Save Attendance",size=(25,2), font=('Helvetica 13'), button_color=('white', 'green')), sg.Button("Back",size=(15,2), font=('Helvetica 13'), button_color=('white', 'red')) ] ]
    window = sg.Window('Mark Attendance', layout, auto_size_buttons=False, element_justification='c', location=(350, 75))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Clock IN Time', 'Clock OUT Time', 'Duration', 'Status']
    attendance = pd.DataFrame(columns=col_names)
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    lecture = sg.popup_get_text('Please Enter Lecture Duration', 'HH:MM:SS')

    while True:
        event, values = window.read(timeout=1)
        window.find_element('_time_').update(f'Date : {datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")}')
        window.find_element('_time_').update(f'Time : {datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")}')
        if event == 'Back':
            c = sg.PopupYesNo(f'Save Attendance ?')
            if c == 'N0':
                cam.release()
                cv2.destroyAllWindows()
                window.close()
            elif c == 'Yes':
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
                attendance.to_csv(fileName, index=False)
                cam.release()
                cv2.destroyAllWindows()
                window.close()
                sg.popup_timed('Attendance Successful')
            break
        elif event == "Save Attendance" or event == sg.WIN_CLOSED:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
            attendance.to_csv(fileName, index=False)
            cam.release()
            cv2.destroyAllWindows()
            window.close()
            sg.popup_timed('Attendance Successful')
            break
        elif event == 'Clock IN':
            check = sg.PopupYesNo(f'{aa[0]} are you clocking In?')
            if check == 'Yes':
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = str(aa)[2:-2]
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, '-', '-', '-']
            elif check == 'N0':
                print('Not clocked IN')
        elif event == 'Clock OUT':
            check = sg.PopupYesNo(f'{aa[0]} are you clocking OUT?')
            if check == 'Yes':
                ts = time.time()
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                attendance.at[attendance[attendance['Id'] == Id].index.values, 'Clock OUT Time'] = timeStamp
                co = attendance.loc[attendance[attendance['Id'] == Id].index.values, 'Clock OUT Time'].to_string().split(' ')
                ci = attendance.loc[attendance[attendance['Id'] == Id].index.values, 'Clock IN Time'].to_string().split(' ')
                FMT = '%H:%M:%S'
                duration = datetime.datetime.strptime(co[-1], FMT) - datetime.datetime.strptime(ci[-1], FMT)
                attendance.at[attendance[attendance['Id'] == Id].index.values, 'Duration'] = duration
                d = datetime.datetime.strptime(lecture, FMT) - datetime.datetime.strptime(str(duration), FMT)
                if int(str(d).split(':')[1]) in range(-5, 6):
                    attendance.at[attendance[attendance['Id'] == Id].index.values, 'Status'] = 'Present'
                else:
                    attendance.at[attendance[attendance['Id'] == Id].index.values, 'Status'] = 'MCR'
            elif check == 'No':
                print('Not clocked OUT')

        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 100:
                aa = df.loc[df['Id'] == Id]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa
            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))
            tt = str(tt)[2:-2]
            if(100-conf) > 67:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            if (100-conf) > 67:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
            elif (100-conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        imgbytes = cv2.imencode(".png", im)[1].tobytes()
        window["image"].update(data=imgbytes)

    cam.release()
    cv2.destroyAllWindows()
    os.system('cls')
