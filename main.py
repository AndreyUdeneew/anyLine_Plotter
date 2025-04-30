import csv

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *

# Глобальные переменные
points = []  # Список точек для хранения координат
outputFilename = ""


# Callback функция для получения координат точек
def draw_line(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))


# Функция для получения значений пикселей по прямой
def get_pixel_values(img, pt1, pt2):
    # Создаем линии между двумя точками
    line_points = cv2.line(np.zeros_like(img), pt1, pt2, (255, 255, 255), 1)

    # Находим координаты всех точек на линии
    indices = np.column_stack(np.where(line_points[:, :, 0] > 0))

    # Получаем значения пикселей для этих точек
    pixel_values = []

    for x, y in indices:
        pixel_values.append(img[y, x, 1])  # Измените индекс (0, 1 или 2) для получения других каналов (B, G или R)

    return pixel_values


def selectOutfile():
    global outputFilename, outputFilenameCSV
    Output = filedialog.askdirectory(parent=window)
    outputFilename = Output + '/OUTPUT.jpeg'
    outputFilenameCSV = Output + '/OUTPUTCSV.csv'
    print(outputFilename)
    text2.insert(INSERT, outputFilename)
    return


# Основная функция
def my_processing():
    global points, outputFilename, outputFilenameCSV
    fileName = askopenfilename(parent=window)
    # print(fileName)
    # print(cv2.getBuildInformation())
    # img = cv2.imread(fileName)
    img = cv2.imdecode(np.fromfile(fileName, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # Открываем окно
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_line)

    while True:
        # Создаем копию изображения для отображения
        img_copy = img.copy()

        # Если есть две точки, рисуем линию и отображаем значения пикселей
        if len(points) == 2:
            cv2.line(img_copy, points[0], points[1], (255, 0, 0), 2)
            cv2.imshow('Image', img_copy)

            # Получаем значения пикселей вдоль линии
            pixel_values = get_pixel_values(img, points[0], points[1])

        cv2.imshow('Image', img_copy)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Escape для выхода
            break
    # Строим график
    with open(outputFilenameCSV, 'w', newline='\n') as f:
        for j in range(len(pixel_values)):
            print(j)
            writer = csv.writer(f)
            writer.writerow([j,pixel_values[j]])
    plt.figure()
    plt.plot(pixel_values, color='red')
    plt.title('Pixel values along the line')
    plt.xlabel('Distance along the line')
    plt.ylabel('Pixel value (G channel)')
    plt.grid()
    plt.show()
    print('outputFilename', outputFilename)
    cv2.imwrite(outputFilename, img_copy)
    # Очистка точек после построения графика
    # points.clear()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    window = Tk()
    window.geometry('1150x650')
    window.title("MassProcessing")
    text1 = Text(width=15, height=1)  # image
    text1.grid(column=1, row=1, sticky=W)
    text2 = Text(width=70, height=1)  # image
    text2.grid(column=1, row=0, sticky=W)
    btn1 = Button(window, text="Select Images", command=my_processing)
    btn1.grid(column=0, row=1, sticky=W)
    btn2 = Button(window, text="Select SavePlace", command=selectOutfile)
    btn2.grid(column=0, row=0, sticky=W)
    window.mainloop()
