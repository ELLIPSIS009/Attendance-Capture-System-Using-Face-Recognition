import PySimpleGUI as sg
import csv

sg.theme('Black')                   
def vcsv():
    filename = sg.PopupGetFile('Get required file', no_window = True,file_types=(("CSV Files","*.csv"),))
    data = []
    #read csv
    with open(filename, "r") as infile:     
        reader = csv.reader(infile)
        for i in range (1):                 
            #get headings
            header = next(reader)
            #read everything else into a list of rows
            data = list(reader)     
    col_layout = [[sg.Text('Attendance Report', font='Helvetica 28', justification='center', pad=(0,10))], [sg.Table(values=data, headings=header,col_widths = (5, 15, 10, 15, 15, 10, 10), auto_size_columns=False,
                    max_col_width = 30, size=(None, len(data)), font='Helvetica 14', justification = 'center', background_color='#303030', text_color='white', alternating_row_color='#505050')],
                    [sg.ReadButton('Back', font = ('Arial', 14, 'bold'), size = (15,1), pad=(0,25))]]

    layout = [[sg.Column(col_layout, size=(1050,500), scrollable=True, element_justification='center')]]

    window = sg.Window('Attendance',layout, grab_anywhere = False, element_justification='c', location=(200, 150))
    event, values = window.Read()
    while True:
        if event == 'Back' or event == sg.WIN_CLOSED:
            window.close()
            break
