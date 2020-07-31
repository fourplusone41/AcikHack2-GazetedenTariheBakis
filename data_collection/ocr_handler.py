# -*- coding: utf-8 -*-

import os,sys
import cv2
import numpy
import pytesseract
from tqdm import tqdm
from pdf2image import convert_from_bytes

class OCR_Handler():
    """
    OCR handler
    """
    def __init__(self, pdf, lang = "tur"):
        self.file = pdf
        self.lang = lang
        self.dpi = 300 # dots per inch
        self.pages = []
        self.text = []

    def imagePreprocessing(self, page):
        #image = cv2.imread(path)
        image = numpy.array(page)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return gray

    def ocr(self):
        print("OCR progress")
        for i, page in tqdm(enumerate(self.pages)):
            img_clean = self.imagePreprocessing(page)
            text = pytesseract.image_to_string(img_clean, self.lang)
            self.text.append(text)

    def pdf2img(self):
        print("convert pdf to images")
        self.pages = convert_from_bytes(self.file, self.dpi)

    def run(self):
        self.pdf2img()
        self.ocr()


