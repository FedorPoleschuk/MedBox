import struct
import tkinter as tk
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ser = serial.Serial('COM3', 1000000)
import re

def main_loop():
    print(1)
    # Создаем окно
    root = tk.Tk()
    root.title("Пример цикла с Tkinter")
    # Функция, которая будет выполняться при нажатии кнопки
    def button_click1():
        ser.write("1\n".encode())

        nonlocal running
        running = True

    def button_click2():
        ser.write("2\n".encode())

        nonlocal running
        running = True
    
    def button_click3():
        ser.write("3\n".encode())

        nonlocal running
        running = True

    random_label = tk.Label(root, text="", font=("Helvetica", 24))
    random_label.pack()

 
    # Создаем кнопку
    button = tk.Button(root, text="Нажми меня", command=button_click1)
    button.pack()

    button2 = tk.Button(root, text="Нажми меня", command=button_click2)
    button2.pack()

    button3 = tk.Button(root, text="Нажми меня", command=button_click3)
    button3.pack()
    # Устанавливаем флаг для цикла
    running = True

    # Создаем объект Figure из Matplotlib
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("График случайных чисел")
    x_values = []
    y_values = []

    # Создаем виджет Canvas для отображения графика
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Функция для добавления случайных чисел к графику
    def update_random_plot():
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
            ax.plot(x_values, y_values)
            ax.set_title("График случайных чисел")
            canvas.draw()
        except Exception: pass


    # Цикл, который будет выполняться, пока running равно True
    while running:
        update_random_plot()  # Обновляем случайное число
        root.update()  # Обновляем окно

    root.destroy()  # Закрываем окно при завершении цикла


if __name__ == "__main__":
    main_loop()
