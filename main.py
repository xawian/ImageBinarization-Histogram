from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from scipy.ndimage import uniform_filter
from math import sqrt
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
    for i in range(0, 255):
        if histogram[i] != 0:
            l_min = i
            break
    for i in range(255, 0, -1):
        if histogram[i] != 0:
            l_max = i
            break
    for i in range (0, 255):
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

def otsu_binarization(image):
    pix = image.load()
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int((pix[x, y][0] + pix[x, y][1] + pix[x, y][2]) / 3)
            histogram[value] += 1
    n_pixels = np.sum(histogram)
    p = [x/n_pixels for x in histogram]
    C0 = np.cumsum(p[:-1])
    C1 = [sum(p[i+1:]) for i in range(255)]
    m0 = [sum(i * p[i] / C0[k] for i in range(k + 1)) if C0[k] != 0 else 0 for k in range(255)]
    m1 = [sum(i * p[i] / C1[k] for i in range(k + 1, 255)) if C1[k] != 0 else 0 for k in range(255)]
    sigma_squared = [C0[k] * C1[k] * (m0[k] - m1[k]) ** 2 for k in range(255)]
    k_star = np.argmax(sigma_squared)
    binarization_average(original, k_star)
    window['TRESH'].update(value=k_star)

def niblack_binarization(image, window_size, k):
    # Convert the image to grayscale
    gray_image = image.convert('L')
    gray_np = np.asarray(gray_image, dtype=np.float64)

    # Calculate the local mean and standard deviation using a window_size x window_size window
    mean_img = uniform_filter(gray_np, (window_size, window_size))
    sqr_img = uniform_filter(gray_np ** 2, (window_size, window_size))
    stddev_img = np.sqrt(sqr_img - mean_img ** 2)

    # Calculate the Niblack threshold for each pixel
    threshold_img = mean_img + k * stddev_img

    # Binarize the image using the Niblack threshold
    binary_image = np.zeros_like(gray_np, dtype=np.uint8)
    binary_image[gray_np > threshold_img] = 255

    # Convert the binary image back to a PIL Image
    binary_pil_image = Image.fromarray(binary_image)

    # Update the image in the GUI
    bio = BytesIO()
    binary_pil_image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())



def sauvola_binarization(image, window_size, k, R=128):
    # Convert the image to grayscale
    gray_image = image.convert('L')
    gray_np = np.asarray(gray_image, dtype=np.float64)

    # Calculate the local mean and standard deviation using a window_size x window_size window
    mean_img = uniform_filter(gray_np, (window_size, window_size))
    sqr_img = uniform_filter(gray_np ** 2, (window_size, window_size))
    stddev_img = np.sqrt(sqr_img - mean_img ** 2)

    # Calculate the Sauvola threshold for each pixel
    threshold_img = mean_img * (1 + k * (stddev_img / R - 1))

    # Binarize the image using the Sauvola threshold
    binary_image = np.zeros_like(gray_np, dtype=np.uint8)
    binary_image[gray_np > threshold_img] = 255

    # Convert the binary image back to a PIL Image
    binary_pil_image = Image.fromarray(binary_image)

    # Update the image in the GUI
    bio = BytesIO()
    binary_pil_image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())


def bernsen(image, neighbourhood_size, contrast_threshold, mid_gray_value):
    image = image.convert("L")
    pix = image.load()
    new_image = Image.new('RGB', image.size)
    new_pix = new_image.load()
    N = neighbourhood_size // 2
    width, height = image.size
    for x in range(width):
        for y in range(height):
            neighbourhood = []
            for i in range(max(0, x - N), min(width, x + N + 1)):
                for j in range(max(0, y - N), min(height, y + N + 1)):
                    neighbourhood.append(pix[i, j])
            max_val = np.max(neighbourhood)
            min_val = np.min(neighbourhood)
            if max_val - min_val < contrast_threshold:
                if mid_gray_value <= 128:
                    new_pix[x, y] = (0, 0, 0)
                else:
                    new_pix[x, y] = (255, 255, 255)
            else:
                if pix[x, y] >= (max_val + min_val) // 2:
                    new_pix[x, y] = (255, 255, 255)
                else:
                    new_pix[x, y] = (0, 0, 0)
    bio = BytesIO()
    new_image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())


def median_filter(image, filter_size):
    # Convert the image to grayscale and then to a NumPy array
    data = np.asarray(image.convert('L'))

    temp = []
    indexer = filter_size // 2
    height, width = data.shape
    data_final = np.zeros((height, width))
    for i in range(height):

        for j in range(width):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > height - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > width - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])
            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []

    # Convert the float array to uint8
    data_final = (data_final * 255).astype(np.uint8)

    # Create an Image object from the NumPy array
    img = Image.fromarray(data_final)

    # Save the image
    bio = BytesIO()
    img.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())

def pixelate(image, pixel_size):
    # Convert the image to a NumPy array
    data = np.asarray(image)

    # Get the size of the image
    height, width, _ = data.shape

    # Create a new image with the same size as the original image
    new_image = Image.new('RGB', (width, height))

    # Loop over the image and replace each pixel
    for i in range(0, height, pixel_size):
        for j in range(0, width, pixel_size):
            # Get the color of the pixel
            r, g, b = data[i][j]
            # Draw a rectangle with the color of the pixel
            new_image.paste(Image.new('RGB', (pixel_size, pixel_size), (r, g, b)), (j, i))

    # Save the pixelated image
    bio = BytesIO()
    new_image.save(bio, format='PNG')
    window['IMAGE'].update(data=bio.getvalue())








control_gui = sg.Column([
    [sg.Frame('Treshold', layout = [[sg.Slider(range = (0, 255), orientation = 'h', key = 'TRESH')]])],
    [sg.Checkbox('R', key = 'R', enable_events=True), sg.Checkbox('G', key = 'G', enable_events=True), sg.Checkbox('B', key = 'B', enable_events=True),
     sg.Checkbox('Average', key = 'AVG', enable_events=True)],
    [sg.Button('Binarization', key = 'BINARIZATION'), sg.Button('Histogram', key = 'HISTOGRAM'), sg.Button('Histogram Streching', key = 'STRECHING')],
    [sg.Button('Histogram Equalization', key = 'EQ'), sg.Button('Otsu', key = 'OTSU'), sg.Button('Niblack', key = 'NIBLACK')],
    [sg.Button('Sauvola', key = 'SAUVOLA'), sg.Button('Bersen', key='BERSEN'), sg.Button('Median', key='MEDIAN'), sg.Button('Pixelate', key="PIXELATE"),
     sg.Button('Kuwahara', key='KUWAHARA')],
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

    if event == 'KUWAHARA':
        # kuwahara_filter(original, 5)
        pass

    if event == 'OTSU':
        otsu_binarization(original)

    if event == 'BERSEN':
        bernsen(original, 15, 30, 128)

    if event == 'NIBLACK':
        niblack_binarization(original, window_size=15, k=-0.2)

    if event == 'SAUVOLA':
        sauvola_binarization(original, window_size=15, k=0.2, R=128)

    if event == 'STRECHING':
        histogram_streching(original, values['TRESH'])

    if event == 'MEDIAN':
        median_filter(original, 3)

    if event == 'RESET':
        original = Image.open(image_path)
        bio = BytesIO()
        original.save(bio, format='PNG')
        window['IMAGE'].update(data=bio.getvalue())

    if event == 'SAVE':
        save_path = sg.popup_get_file('Save', save_as = True, no_window = True) + '.png'
        original.save(save_path, 'PNG')

    if event == 'PIXELATE':
        pixelate(original, 10)

    if event == 'UPLOAD':
        image_path = sg.popup_get_file('Upload', no_window = True)
        original = Image.open(image_path)
        bio = BytesIO()
        original.save(bio, format='PNG')
        window['IMAGE'].update(data=bio.getvalue())


window.close()




