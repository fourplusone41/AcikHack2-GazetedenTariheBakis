#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os,sys
from pdf2image import convert_from_path
from OCR import Ocr


# In[2]:


def fileName(path):
    image = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.endswith(".png") and entry.is_file():
                image.append(entry.name) 
    return image



# In[3]:


def pdf2png(dirName,pdfFileName):
    dpi = 500 # dots per inch
    pdf_file = str(dirName)+"/"+str(pdfFileName)
    pages = convert_from_path(pdf_file ,dpi )
    for i in range(len(pages)):
        page = pages[i]
        page.save(dirName+"/"+str('output_{}.png'.format(i)), 'PNG')


# In[4]:


def createDir(dirName):
    try:
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")


# In[5]:


dirName = 'DataSet'
pdfFileName = "anadolu_1938_kanunusani_2_.pdf"
createDir(dirName)
pdf2png(dirName,pdfFileName)
image = fileName(dirName)


# In[6]:


Ocr(dirName,image)


# In[ ]:




