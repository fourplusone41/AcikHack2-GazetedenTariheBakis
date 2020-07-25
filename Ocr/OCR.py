# -*- coding: utf-8 -*-

import pytesseract
import cv2



def imagePreprocessing(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return gray
   

def Ocr(dirName,image):
    for i in image:
        ocrImage =dirName+"/"+str(i) 
        text = pytesseract.image_to_string(imagePreprocessing(ocrImage),lang="tur")
        f = open(ocrImage+str(".txt"), "a")
        f.write(text)
        f.close()
