from PIL import Image


def binarization_average(image, treshold): #average of RGB
    for x in range(image.width):
        for y in range(image.height):
            averageRGB = (pix[x, y][1] + pix[x, y][2] + pix[x, y][2]) / 3
            if averageRGB > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def binarization_R(image, treshold): #binarization on canal R
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][0] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def binarization_G(image, treshold): #binarization on canal G
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][1] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


def binarization_B(image, treshold): #binarization on canal B
    for x in range(image.width):
        for y in range(image.height):
            if pix[x,y][2] > treshold:
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)


im = Image.open("samples/baboon.jpg")
pix = im.load()
binarization_average(im, 128)
im.show()





