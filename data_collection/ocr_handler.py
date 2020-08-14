# -*- coding: utf-8 -*-

import os,sys
import cv2
import numpy
import pytesseract
from tqdm import tqdm
from pdf2image import convert_from_bytes

from queue import Queue
from threading import Thread



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
        # Queue for multithreading
        self.ocr_queue = Queue()
        self.workers = [
            Thread(target=self.ocr, daemon=True)
            for _ in range(2)
        ]

    def imagePreprocessing(self, page):
        #image = cv2.imread(path)
        image = numpy.array(page)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return gray

    def ocr(self):
        #print("OCR progress")
        #while True:
        #    page = self.ocr_queue.get()
        for i, page in tqdm(enumerate(self.pages)):
            img_clean = self.imagePreprocessing(page)
            text = pytesseract.image_to_string(img_clean, self.lang)
            self.text.append(text)

            self.ocr_queue.task_done()

    def pdf2img(self):
        #print("convert pdf to images")
        self.pages = convert_from_bytes(self.file, self.dpi)
        for page in self.pages:
            self.ocr_queue.put(page)

    def run(self):
        self.pdf2img()
        self.ocr()
        
        #for w in self.workers:
        #    w.start()

        #for w in tqdm(self.workers):
        #    w.join()*/


