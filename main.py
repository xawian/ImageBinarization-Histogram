from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from io import BytesIO


def binarization_average(image, treshold):
    pix = image.load()
    for x in range(image.width):
        for y in range(image.height):
            averageRGB = (pix[x, y][1] + pix[x, y][2] + pix[x, y][2]) / 3
            if averageRGB > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)
    bio = BytesIO()
    image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())


def binarization_R(image, treshold):
    pix = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][0] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)
    bio = BytesIO()
    image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())


def binarization_G(image, treshold):
    pix = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][1] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)
    bio = BytesIO()
    image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())


def binarization_B(image, treshold):
    pix = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][2] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)
    bio = BytesIO()
    image.save(bio, format = 'PNG')
    window['IMAGE'].update(data = bio.getvalue())


def generate_histogram_R(image):
    pix = image.load()
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int(pix[x, y][0])
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram canal R")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()


def generate_histogram_G(image):
    pix = image.load()
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int(pix[x, y][1])
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram canal G")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()


def generate_histogram_B(image):
    pix = image.load()
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int(pix[x, y][2])
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram canal B")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()


def generate_histogram_average(image):
    pix = image.load()
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int((pix[x, y][0] + pix[x, y][1] + pix[x, y][2]) / 3)
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram average")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()

def calculate_LUT(histogram, treshold):
    l_min = 0
    l_max = 255
    for i in range(0, 256):
        if histogram[i] != 0:
            l_min = i
            break
    for i in range(256, 0, -1):
        if histogram[i] != 0:
            l_max = i
            break
    for i in range (0, 256):
        histogram[i] = int((treshold / (l_max - l_min)) * (i - l_min))
    return histogram

def histogram_streching(image, treshold):
    pix = image.load()
    histogram_red = np.zeros([256], dtype=int)
    histogram_green = np.zeros([256], dtype=int)
    histogram_blue = np.zeros([256], dtype=int)
    for x in range(image.width):
        for y in range(image.height):
            histogram_red[int(pix[x, y][0])] += 1
            histogram_green[int(pix[x, y][1])] += 1
            histogram_blue[int(pix[x, y][2])] += 1
    LUTred = calculate_LUT(histogram_red, treshold)
    LUTblue = calculate_LUT(histogram_blue, treshold)
    LUTgreen = calculate_LUT(histogram_green, treshold)
    for x in range(image.width):
        for y in range(image.height):
            pix[x,y] = (LUTred[pix[x,y][0]], LUTgreen[pix[x,y][1]], LUTblue[pix[x,y][2]])
    bio = BytesIO()
    image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())

def calculate_LUT_eq(histogram, D):
    distribution = D[0]
    # print(D)
    for i in range(0, 256):
        if D[i] != 0:
            distribution = D[i]
            break
    # print(distribution)
    for i in range (0, 256):
        histogram[i] = int(((D[i] - distribution) / (1 - distribution)) * 254)
    return histogram

def histogram_equalization(image):
    pix = image.load()
    histogram_red = np.zeros([256], dtype=int)
    histogram_green = np.zeros([256], dtype=int)
    histogram_blue = np.zeros([256], dtype=int)
    for x in range(image.width):
        for y in range(image.height):
            histogram_red[int(pix[x, y][0])] += 1
            histogram_green[int(pix[x, y][1])] += 1
            histogram_blue[int(pix[x, y][2])] += 1
    D_red = [(x + sum(histogram_red[:i]))/np.sum(histogram_red) for i, x in enumerate(histogram_red)]
    D_blue = [(x + sum(histogram_blue[:i]))/np.sum(histogram_blue) for i, x in enumerate(histogram_blue)]
    D_green = [(x + sum(histogram_green[:i]))/np.sum(histogram_green) for i, x in enumerate(histogram_green)]
    LUTred = calculate_LUT_eq(histogram_red, D_red)
    LUTblue = calculate_LUT_eq(histogram_blue, D_blue)
    LUTgreen = calculate_LUT_eq(histogram_green, D_green)
    for x in range(image.width):
        for y in range(image.height):
            pix[x,y] = (LUTred[pix[x,y][0]], LUTgreen[pix[x,y][1]], LUTblue[pix[x,y][2]])
    bio = BytesIO()
    image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())





control_gui = sg.Column([
    [sg.Frame('Treshold', layout = [[sg.Slider(range = (0, 255), orientation = 'h', key = 'TRESH')]])],
    [sg.Checkbox('R', key = 'R', enable_events=True), sg.Checkbox('G', key = 'G', enable_events=True), sg.Checkbox('B', key = 'B', enable_events=True),
     sg.Checkbox('Average', key = 'AVG', enable_events=True)],
    [sg.Button('Binarization', key = 'BINARIZATION'), sg.Button('Histogram', key = 'HISTOGRAM'), sg.Button('Histogram Streching', key = 'STRECHING')],
    [sg.Button('Histogram Equalization', key = 'EQ')],
    [sg.Button('Save image', key = 'SAVE'), sg.Button('Upload image', key = 'UPLOAD'), sg.Button('Reset', key = 'RESET')],
])

image_path = 'samples/lenna.png'
image_gui = sg.Column([[sg.Image(image_path, key = 'IMAGE')]])
layout = [[control_gui, image_gui]]
original = Image.open(image_path)
window = sg.Window('Biometrics', layout)

while True:
    event, values = window.read(timeout=50)

    if event in ['R', 'G', 'B', 'AVG']: #only one checkbox
        for key in ['R', 'G', 'B', 'AVG']:
            if key != event:
                window[key].update(False)

    if event == sg.WIN_CLOSED:
        break

    if event == 'BINARIZATION' and values['B'] == True:
        binarization_B(original, values['TRESH'])

    if event == 'BINARIZATION' and values['R'] == True:
        binarization_R(original, values['TRESH'])

    if event == 'BINARIZATION' and values['G'] == True:
        binarization_G(original, values['TRESH'])

    if event == 'BINARIZATION' and values['AVG'] == True:
        binarization_average(original, values['TRESH'])

    if event == 'HISTOGRAM' and values['AVG'] == True:
        generate_histogram_average(original)

    if event == 'HISTOGRAM' and values['R'] == True:
        generate_histogram_R(original)

    if event == 'HISTOGRAM' and values['G'] == True:
        generate_histogram_G(original)

    if event == 'HISTOGRAM' and values['B'] == True:
        generate_histogram_B(original)

    if event == 'EQ':
        histogram_equalization(original)

    if event == 'STRECHING':
        histogram_streching(original, values['TRESH'])

    if event == 'RESET':
        original = Image.open(image_path)
        bio = BytesIO()
        original.save(bio, format='PNG')
        window['IMAGE'].update(data=bio.getvalue())

    if event == 'SAVE':
        save_path = sg.popup_get_file('Save', save_as = True, no_window = True) + '.png'
        original.save(save_path, 'PNG')

    if event == 'UPLOAD':
        image_path = sg.popup_get_file('Upload', no_window = True)
        original = Image.open(image_path)
        bio = BytesIO()
        original.save(bio, format='PNG')
        window['IMAGE'].update(data=bio.getvalue())


window.close()




