import struct
import tkinter as tk
import serial
from matplotlib.figure import Figure
from PIL import Image as Img
from PIL import ImageTk  # $ pip install pillow
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ser = serial.Serial('COM3', 1000000)
import re
import cv2

def main_loop():
    print(1)
    # Создаем окно
    root = tk.Tk(   )
    # root.attributes("-fullscreen", True)
    root.title("Пример цикла с Tkinter")
    root.geometry('800x480')


    frame1 = tk.Frame(master=root, height=100 )
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

    frame2= tk.Frame(master=root, height=100)
    frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=False)
    # Функция, которая будет выполняться при нажатии кнопки
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

        ser.reset_input_buffer()
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
        canvas.get_tk_widget().pack_forget()
        camera.pack_forget()
        run = False
        cap.release()







    tmp = 0

    # random_label = tk.Label(root, text="", font=("Helvetica", 24))
    # random_label.pack()


    # Создаем кнопку
    image1 = ImageTk.PhotoImage(file="stethoscope.png")
    button1 = tk.Button(frame1, image=image1,text="Нажми меня", command=button_click1)
    button1.pack()
    # button1['state'] = 'disabled'


    image2 = ImageTk.PhotoImage(file="ear.png")
    button2 = tk.Button(frame1, image=image2,
                        text="Нажми меня", command=button_click2)
    button2.pack()
    if 2 in buffer:
        button2['state'] = 'disabled'



    image3 = ImageTk.PhotoImage(file="pulse-oximeter.png")
    button3 = tk.Button(frame1, image=image3, command=button_click3)
    button3.pack()


    image4 = ImageTk.PhotoImage(file="ecg-lines.png")
    button4 = tk.Button(frame1, image=image4, command=button_click4)
    button4.pack()

    image5 = ImageTk.PhotoImage(file="red-blood-cells.png")
    button5 = tk.Button(frame1, image=image5, command=button_click5)
    button5.pack()

    image6 = ImageTk.PhotoImage(file="temperature.png")
    button6 = tk.Button(frame1, image=image6, command=button_click6)
    button6.pack()

    image7 = ImageTk.PhotoImage(file="arm.png")
    button7 = tk.Button(frame1, image=image7, command=button_click7)
    button7.pack()

    button_start = tk.Button(frame2, text="Start", command=button_start_click)
    button_start.pack(side=LEFT)

    button_stop = tk.Button(frame2, text="Stop", command=button_stop_click)
    button_stop.pack(side=LEFT)
    button_start['state'] = 'disabled'
    button_stop['state'] = 'disabled'

    # Устанавливаем флаг для цикла
    running = True

    # Создаем объект Figure из Matplotlib
    fig = Figure(figsize=(7, 5), dpi=100)
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
        print((response))
        # random_label.config(text=str(response))

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

    def update_camera():
        _, frame = cap.read()

    # Convert image from one color space to other
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Capture the latest frame and transform to image
        captured_image = Img.fromarray(opencv_image)


        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photoimage in the label
        camera.photo_image = photo_image

        # Configure image in the label
        camera.configure(image=photo_image)

        # Repeat the same process after every 10 seconds
        # width, height =  # Width of camera, #Height of Camera


        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
    run = False

    # Цикл, который будет выполняться, пока running равно True
    while running:
        if run:
            if tmp == 0:
                    camera.pack_forget()
                    canvas.get_tk_widget().pack_forget()

            if tmp==2:
                    camera.pack()
                    canvas.get_tk_widget().pack_forget()
                    update_camera()  # Обновляем случайное число

            if tmp!=0 and tmp!=2:
                    canvas.get_tk_widget().pack()
                    camera.pack_forget()
                    update_plot()
        


        root.update()  # Обновляем окно

    root.destroy()  # Закрываем окно при завершении цикла


if __name__ == "__main__":
    
    buffer=[]
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        buffer.append(2)
        


    # response = ser.readline().decode().strip()
    # print("response" ,response)

    main_loop()
