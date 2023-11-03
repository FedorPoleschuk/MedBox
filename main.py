import smtplib
# import smtplibdef send_mail():
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import shutil
import os
from transliterate import translit, get_available_language_codes
import struct
import tkinter as tk
import serial
from matplotlib.figure import Figure
import pandas as pd
from PIL import Image as Img
from PIL import ImageTk  # $ pip install pillow
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ser = serial.Serial('/dev/ttyUSB0', 1000000)
import re
import cv2
import datetime
import time
layout = {
    'en':[
        ['1','2','3','4','5','6','7','8','9','0','←'],
        ['q','w','e','r','t','y','u','i','o','p'],
        ['a','s','d','f','g','h','j','k','l'],
        ['z','x','c','v','b','n','m','.','@'],
        ['Lang','Space']
    ],
    'rus':[
        ['1','2','3','4','5','6','7','8','9','0','.','←'],
        ['й','ц','у','к','е','н','г','ш','щ','з','х','ъ'],
        ['ф','ы','в','а','п','р','о','л','д','ж',"э"],
        ['я','ч','с','м','и','т','ь','б','ю','ё'],
        ['Lang','Space']]
}
text=""
state="rus"
def main_loop():
    entry=""
    INIT = ""
    tmp = 0
    isRecord = 0
    timestamp = ""
    path = ""
    username=""
    email =""
    path_to_csv = ""
    path_to_avi = ""
    shape = (0, 0)
    font_entry = ('Arial', 20)
    label_font = ('Arial', 30, 'bold')
    running = True
    sensor = {1: "Sthetoscope", 2: "Othoscope", 3: "PO",
              4: "ECG", 5: "Glucose ", 6: "Temperature", 7: "BP"}

    layout = {
    'en':[
        ['1','2','3','4','5','6','7','8','9','0','←'],
        ['q','w','e','r','t','y','u','i','o','p'],
        ['a','s','d','f','g','h','j','k','l'],
        ['z','x','c','v','b','n','m','.','@'],
        ['Lang','Space']
    ],
    'rus':[
        ['1','2','3','4','5','6','7','8','9','0','.','←'],
        ['й','ц','у','к','е','н','г','ш','щ','з','х','ъ'],
        ['ф','ы','в','а','п','р','о','л','д','ж',"э"],
        ['я','ч','с','м','и','т','ь','б','ю','ё'],
        ['Lang','Space']]
}

    # Создаем окно
    root = tk.Tk(   )
    # root.attributes("-fullscreen", True)
    root.title("MedBox")
    root.geometry('1920x1080')
    
    


    TopBar= tk.Frame(master=root)
    TopBar.pack(fill=tk.X, side=tk.TOP, expand=False)
    TopBar.pack_forget()

    BottomBar = tk.Frame(master=root)
    BottomBar.pack(side=tk.BOTTOM, expand=False)
    BottomBar.pack_forget()

    sideBar = tk.Frame(master=root)
    sideBar.pack(fill=tk.Y, side=tk.LEFT, expand=True)
    sideBar.pack_forget()

    SignBar = tk.Frame(master=root)
    SignBar.pack(fill=tk.Y,expand=True)

    keyframe  = tk.Frame(master=SignBar)
    keyframe.grid_forget()

    keysframe_rus = tk.Frame(keyframe)
    keysframe_rus.grid(row=3)

    keysframe_en = tk.Frame(keyframe)
    keysframe_en.grid(row=3)

    keysframe_en.grid_forget()
    def key(self):
        global state
        global text
        match state:
            case "en":
                state = "en"
                match self:
                    case "Lang":
                        state = "rus"
                    case "Space":
                        if entry == 'email':
                            email_entry.insert(END," ")
                        if entry == 'username':
                            username_entry.insert(END," ")
                        
                    case "←": 
                        if entry == 'email':
                            email_entry.delete(len(email_entry.get())-1,END)
                        if entry == 'username':
                            username_entry.delete(len(username_entry.get())-1,END) 
                    case _:
                        text=text+self
                        if entry == 'email':
                            email_entry.insert(END,self)
                        if entry == 'username':
                            username_entry.insert(END,self)

            case "rus":
                state = "rus"
                match self:     
                    case "Lang":
                        state = "en"
                    case "Space":
                        if entry == 'email':
                            email_entry.insert(END," ")
                        if entry == 'username':
                            username_entry.insert(END," ")          
                    case "←": 
                        if entry == 'email':
                            email_entry.delete(len(email_entry.get())-1,END)
                        if entry == 'username':
                            username_entry.delete(len(username_entry.get())-1,END)  
                    case _:
                        text = text + self
                        if entry == 'email':
                            email_entry.insert(END,self)
                        if entry == 'username':
                            username_entry.insert(END,self)
        match state:
            case "rus":
                keysframe_rus.grid(sticky='s')
                keysframe_en.grid_forget()
            case "en":
                keysframe_rus.grid_forget()
                keysframe_en.grid(sticky='s')
           





    
    # Функция, которая будет выполняться при нажатии кнопки

    def Keyboard():

        for st in layout.keys():
            match st:
                case "en":
                    frame =  keysframe_en
                case "rus":
                    frame =  keysframe_rus
            
            rows = layout.get(st)

            for idx, row in enumerate(rows):
                gap =0

                for jdx, col in enumerate(row):
                    width=7
                    columnspan=1
                    colunm = jdx + gap
                    label = col
                    match col: 
                    
                        case "Lang":
                            columnspan=2
                            width = 20
                            gap +=1
                            Button(frame, text=label,width=width, command=lambda name=label: key(name)).grid(row=idx, pady=3,column=colunm,columnspan=columnspan)
                        case "Space":
                            columnspan=11
                            width = 80
                            gap+=7
                            Button(frame, text=label,width=width, command=lambda name=label: key(name)).grid(row=idx, column=colunm,columnspan=columnspan)
                        case _:
                            Button(frame, text=label,width=width,command=lambda name=label: key(name)).grid(row=idx, pady=3,column=colunm,columnspan=columnspan)


    def patient_info():
        nonlocal entry
        entry = ''
        button_send['state'] = 'disabled'

        global INIT
        INIT = 1
        button_stop_click()
        sideBar.pack_forget()
        TopBar.pack_forget()
        BottomBar.pack_forget()
        for c in range(3): SignBar.columnconfigure(index=c, weight=1)
        for r in range(3): 
            if r==2 or r==0:
                SignBar.rowconfigure(index=r, weight=2)
            else:  SignBar.rowconfigure(index=r, weight=1)
        SignBar.pack(fill=tk.Y,expand=True)
        
        
        keyframe.grid(sticky=S)


        Keyboard()

    def button_click1():
        nonlocal tmp
        nonlocal running
        button_stop_click()
        running = True
        tmp = 1

    def button_click2():
        nonlocal tmp
        nonlocal running
        button_stop_click()
        tmp = 2
    
    def button_click3():
        nonlocal tmp
        nonlocal running
        ser.write("3\n".encode())
        button_stop_click()
        tmp = 3

    def button_click4():
        nonlocal tmp
        nonlocal running
        ser.write("4\n".encode())
        button_stop_click()
        running = True
        tmp = 4

    def button_click5():
        nonlocal tmp
        nonlocal running
        ser.write("5\n".encode())
        button_stop_click()
        running = True
        tmp = 5

    def button_click6():
        nonlocal tmp
        nonlocal running
        ser.write("6\n".encode())
        button_stop_click()
        running = True
        tmp = 6

    def button_click7():
        nonlocal tmp
        nonlocal running
        ser.write("7\n".encode())
        button_stop_click()
        running = True
        tmp = 7

    def button_start_click():
        global cap
        cap=cv2.VideoCapture(0)
        # ser.reset_input_buffer()
        nonlocal run
        nonlocal x_values
        nonlocal y_values
        x_values = []
        y_values = []
        button_stop.pack()
        button_stop['state'] = 'active'
        button_start['state'] = 'disabled'
        run=True

    def button_stop_click():
        nonlocal run
        button_stop.pack()
        button_start['state'] = 'active'
        button_stop['state'] = 'disabled'
        button_stop_record_click()
        canvas.get_tk_widget().pack_forget()
        camera.pack_forget()
        button_start_record.pack_forget()
        button_stop_record.pack_forget()
        run = False
        cap.release()

    def button_start_record_click():
        nonlocal isRecord
        nonlocal tmp
        button_stop_record['state'] = 'active'
        button_start_record['state'] = 'disabled'
        nonlocal timestamp

        timestamp = time.strftime("%d_%m_%Y_%H_%M_%S", time.localtime())
        if tmp != 2:
            nonlocal path_to_csv
            path_to_csv = path + "/" + sensor[tmp] + '_' + timestamp + '.csv'
            with open(path_to_csv, 'w') as f:
                f.close()
            df = pd.DataFrame({'timestamp': [timestamp[-13:]],
                                't': ['        '],
                                'values': ['        ']})
            df.to_csv(path_to_csv, sep='\t', index=False)
        else:
            nonlocal shape
            nonlocal path_to_avi
            global video_avi

            path_to_avi = path +"/"+ sensor[tmp] + '_' + timestamp + '.avi'
            video_avi = cv2.VideoWriter(path_to_avi,cv2.VideoWriter_fourcc('M','J','P','G'), 20.0, (w, h))
        isRecord = 1
         
    def button_stop_record_click():
        try:
            if len(os.listdir(path)) == 0:
                print("Directory is empty")


            else:
                button_send['state'] = 'active'
        except Exception: pass

        

        nonlocal isRecord

        button_start_record['state'] = 'active'
        button_stop_record['state'] = 'disabled'
        video_avi.release()
        isRecord = 0

    def recording_buttons():
        button_start_record.pack(side=RIGHT)
        button_stop_record.pack(side=RIGHT)

    def recording():
        nonlocal path
        nonlocal path_to_csv
        df = pd.DataFrame({'timestamp': ['          '],
                            't': [x_values[-1]],
                            'values': [y_values[-1]]})
        df.to_csv(path_to_csv, sep='\t',index=False, header=False, mode='a')

    def sign_btn_click():
        nonlocal username
        nonlocal email
        nonlocal path

        username = username_entry.get()
        email = email_entry.get()
        patient_label['text'] = username
        patient_email_label['text'] = email

        sideBar.pack(fill=tk.Y, side=tk.LEFT, expand=False)
        TopBar.pack(fill=tk.X, side=tk.TOP, expand=False)
        BottomBar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

        patient_label.pack(side=tk.LEFT, padx=30, expand=False)
        patient_email_label.pack(side=tk.LEFT, padx=30, expand=False)
        
        path = re.sub(r"\s+", "", translit(username, 'ru', reversed=True))+time.strftime("%d%m%Y%H%M", time.localtime())
        os.makedirs(path, mode=0o777, exist_ok=False)
        

        SignBar.pack_forget()

    def restart_button_click():
        nonlocal path
        shutil.rmtree(path)
        path =""
        patient_info()

    def entry_click(event):
        nonlocal entry
        entry = 'email'
    def entry_click1(event):
        nonlocal entry
        entry = 'username'

    def button_send_click():
        shutil.make_archive("Analysis", 'zip', path)
        msg = MIMEMultipart()


        body_part = MIMEText("MESSAGE_BODY", 'plain')
        msg['Subject'] = "ANALYSIS " + username
        msg['From'] = "healthcatalyst"
        msg['To'] = email
        # Add body to email
        msg.attach(body_part)
        # open and read the file in binary
        with open("Analysis.zip", 'rb') as file:
                # Attach the file with filename to the email
            msg.attach(MIMEApplication(file.read(), Name='Analysis.zip'))
        try:
            # подключаемся к почтовому сервису
            smtp = smtplib.SMTP("smtp.yandex.ru", 465)
            smtp.starttls()
            smtp.ehlo()
            # логинимся на почтовом сервере
            smtp.login("healthcatalyst@yandex.ru", "jthnjbkptshvgtsn")
            # пробуем послать письмо
            smtp.sendmail(msg['From'], msg['To'],  msg.as_string())


        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            smtp.quit()
        restart_button_click()
        
       
       
    
    

    s = Style()
    s.configure('.', font=('Arial',30,'bold'))

    # START FORM
    name_frame=tk.Frame(master=SignBar)
    name_frame.grid()

    email_frame = tk.Frame(master=SignBar,pady=10)
    email_frame.grid()

    username_label = Label(name_frame, text='ФИО',
                           font=label_font)
    username_label.pack(anchor="w",side=tk.LEFT)

    username_entry = Entry(name_frame,  font=font_entry)
    username_entry.focus_set()
    username_entry.pack(anchor="center", side=tk.LEFT)

    email_label = Label(email_frame, text='Email',
                    font=label_font)
    email_label.pack(anchor="w", side=tk.LEFT)
    email_entry = Entry(email_frame, font=font_entry)
    email_entry.pack(anchor="center", side=tk.LEFT)

    sign_btn = Button(SignBar, text='Начать', command=sign_btn_click)
    sign_btn.grid()

    


    patient_label = Label(BottomBar, text="username",
                          font=label_font)
    patient_email_label = Label(BottomBar, text="email",
                          font=label_font)
    


    # SENSOR BUTTON

    image1 = ImageTk.PhotoImage(file="./stethoscope.png")
    button1 = Button(sideBar, image=image1, text="Нажми меня",
                     command=button_click1)
    button1.pack()
    if 1 in buffer:
        button2['state'] = 'disabled'

    image2 = ImageTk.PhotoImage(file="ear.png")
    button2 = Button(sideBar, image=image2,
                        text="Нажми меня", command=button_click2)
    button2.pack()
    print(Button)
    if 2 in buffer:
        button2['state'] = 'disabled'

    image3 = ImageTk.PhotoImage(file="pulse-oximeter.png")
    button3 = Button(sideBar, image=image3, command=button_click3)
    button3.pack()

    image4 = ImageTk.PhotoImage(file="ecg-lines.png")
    button4 = Button(sideBar, image=image4, command=button_click4)
    button4.pack()

    image5 = ImageTk.PhotoImage(file="red-blood-cells.png")
    button5 = Button(sideBar, image=image5, command=button_click5)
    button5.pack()

    image6 = ImageTk.PhotoImage(file="temperature.png")
    button6 = Button(sideBar, image=image6, command=button_click6)
    button6.pack()

    image7 = ImageTk.PhotoImage(file="arm.png")
    button7 = Button(sideBar, image=image7, command=button_click7)
    button7.pack()

    button_start = Button(TopBar, text="Start", command=button_start_click)
    button_start.pack(side=LEFT)

    button_stop = Button(TopBar, text="Stop", command=button_stop_click)
    button_stop.pack(side=LEFT)
    button_start['state'] = 'disabled'
    button_stop['state'] = 'disabled'


    button_restart = Button(BottomBar, text="Restart",
                            command=restart_button_click)
    button_restart.pack(side=tk.LEFT, fill=tk.X)
    button_send = Button(BottomBar, text="Send",
                            command=button_send_click)
    button_send.pack(side=tk.RIGHT, fill=tk.X)
    button_send['state'] = 'disabled'

    

    button_start_record = Button(TopBar, text="Start recording", command=button_start_record_click)
    button_stop_record = Button(TopBar, text="Stop recording", command=button_stop_record_click)
    button_start_record['state'] = 'active'
    button_stop_record['state'] = 'disabled'

    # Устанавливаем флаг для цикла

    # Создаем объект Figure из Matplotlib
    fig = Figure(figsize=(16, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("График случайных чисел")
    x_values = []
    y_values = []

    # Создаем виджет Canvas для отображения графика
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack_forget()

    camera = Label(root)
    camera.pack_forget()

    # Функция для добавления случайных чисел к графику
    def update_plot():
        response = ser.readline().decode('latin-1').strip()
        value = re.findall(r'\d+', response)
        print(response)
       
        try: 
            print(value[0])
            nonlocal x_values, y_values
            x_values.append(len(x_values) + 1)
            y_values.append(int(value[0]))            
            ax.clear()
            ax.plot(x_values[-100:], y_values[-100:])
            # ax.set_title("График случайных чисел")
            ax.grid(color='grey', linestyle='--', linewidth=1)
            canvas.draw()
        except Exception: pass

    def update_camera(rec):
        ret, frame = cap.read()

    # Convert image from one color space to other
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if rec and ret:
            video_avi.write(frame)

        scale_percent = 200  # percent of original size

        width = int(opencv_image.shape[1] * scale_percent / 100)
        height = int(opencv_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # Capture the latest frame and transform to image
        opencv_image = cv2.resize(opencv_image, dim, interpolation=cv2.INTER_AREA)
        captured_image = Img.fromarray(opencv_image)

        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photoimage in the label
        camera.photo_image = photo_image
        camera.configure(image=photo_image)
        
    run = False
    if INIT == "":
        patient_info()

    while running:
        if run:
            recording_buttons()

            if tmp == 0:
                camera.pack_forget()
                canvas.get_tk_widget().pack_forget()

            if tmp==2:
                camera.pack(side=tk.TOP, padx = 300, fill=tk.BOTH, expand=True)
                canvas.get_tk_widget().pack_forget()
                update_camera(isRecord)  # Обновляем случайное число

            if tmp!=0 and tmp!=2:
                canvas.get_tk_widget().pack(side=tk.TOP)
                camera.pack_forget()
                update_plot()
            
            if isRecord and tmp != 2:
                recording()
                print("RECOOOORDING!!!!!!!!!!!!!!!!!!!!!!!RECOOOORDING")

        email_entry.bind("<FocusIn>", entry_click)
        username_entry.bind("<FocusIn>", entry_click1)
        
        root.update()  # Обновляем окно
    
    root.destroy()  # Закрываем окно при завершении цикла

# def send():
#     pass

# def send_email():
#     os.chdir('..')
#     send("Panov_Semen_Stanislavovich")

if __name__ == "__main__":
    
    buffer=[]
    cap = cv2.VideoCapture(0)
    h=int(cap.get(4))
    w=int(cap.get(3))
    video_avi = cv2.VideoWriter("default.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 20.0,(w, h))
    if cap is None or not cap.isOpened():
        buffer.append(2)
        
    

    main_loop()
    # send_email()
