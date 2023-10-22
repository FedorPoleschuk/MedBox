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
    root.title("Пример цикла с Tkinter")
    root.geometry('800x480')


    frame1 = tk.Frame(master=root, height=100 )
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
    # Функция, которая будет выполняться при нажатии кнопки
    def button_click1():
        ser.write("1\n".encode())
        camera.pack_forget
        nonlocal running
        nonlocal tmp
        nonlocal x_values
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()

        running = True
        tmp = 1

    def button_click2():
        ser.write("2\n".encode())
        nonlocal running
        nonlocal tmp
        nonlocal x_values
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()

        running = True
        tmp = 2



    
    def button_click3():
        ser.write("3\n".encode())
        nonlocal running
        nonlocal tmp
        nonlocal x_values 
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()
        running = True
        tmp = 3


    def button_click4():
        ser.write("4\n".encode())
        nonlocal running
        nonlocal tmp
        nonlocal x_values
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()
        camera.pack_forget
        running = True
        tmp = 4



    def button_click5():
        ser.write("5\n".encode())
        nonlocal running
        nonlocal tmp
        nonlocal x_values
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()
        running = True
        tmp = 5

    
    def button_click6():
        ser.write("6\n".encode())
        nonlocal running
        nonlocal tmp

        nonlocal x_values 
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()

        running = True
        tmp = 6


    def button_click7():
        ser.write("7\n".encode())
        nonlocal running
        nonlocal tmp
        nonlocal x_values
        nonlocal y_values
        x_values = []
        y_values = []
        ax.clear()

        running = True
        tmp = 7



    tmp = 0

    random_label = tk.Label(root, text="", font=("Helvetica", 24))
    random_label.pack()


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
    button3 = tk.Button(frame1, image=image3, text="Нажми меня", command=button_click3)
    button3.pack()
    # button3['state'] = 'disabled'


    image4 = ImageTk.PhotoImage(file="ecg-lines.png")
    button4 = tk.Button(frame1, image=image4,
                        text="Нажми меня", command=button_click4)
    button4.pack()

    image5 = ImageTk.PhotoImage(file="red-blood-cells.png")
    button5 = tk.Button(frame1, image=image5,
                        text="Нажми меня", command=button_click5)
    button5.pack()

    image6 = ImageTk.PhotoImage(file="temperature.png")
    button6 = tk.Button(frame1, image=image6,
                        text="Нажми меня", command=button_click6)
    button6.pack()

    image7 = ImageTk.PhotoImage(file="arm.png")
    button7 = tk.Button(frame1, image=image7,
                        text="Нажми меня", command=button_click7)
    button7.pack()
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
    canvas.get_tk_widget().pack()

    camera = Label(root)
    camera.pack()

    # Функция для добавления случайных чисел к графику
    def update_plot():
        response = ser.readline().decode('latin-1').strip()
        print((response))
        random_label.config(text=str(response))

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
        

    # Цикл, который будет выполняться, пока running равно True
    while running:
        if tmp!=2:
            canvas.get_tk_widget().pack()
            camera.pack_forget()
            update_plot()
        else:
            camera.pack()

            canvas.get_tk_widget().pack_forget()

            update_camera()  # Обновляем случайное число
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
