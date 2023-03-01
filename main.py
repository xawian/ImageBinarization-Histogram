from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def binarization_average(image, treshold):
    for x in range(image.width):
        for y in range(image.height):
            averageRGB = (pix[x, y][1] + pix[x, y][2] + pix[x, y][2]) / 3
            if averageRGB > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def binarization_R(image, treshold):
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][0] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def binarization_G(image, treshold):
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][1] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def binarization_B(image, treshold):
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][2] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def generate_histogram_R(image):
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
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int(pix[x, y][1])
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram canal R")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()


def generate_histogram_B(image):
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int(pix[x, y][2])
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram canal R")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()


def generate_histogram_average(image):
    histogram = np.zeros([256])
    for x in range(image.width):
        for y in range(image.height):
            value = int((pix[x, y][0] + pix[x, y][1] + pix[x, y][2]) / 3)
            histogram[value] += 1
    plt.figure()
    plt.title("Histogram canal R")
    plt.bar(np.arange(len(histogram)), histogram)
    plt.ylabel("Number of Pixels")
    plt.xlabel("Pixel Value")
    plt.show()


im = Image.open("samples/baboon.jpg")
pix = im.load()
binarization_average(im,128)
generate_histogram_average(im)
im.show()





