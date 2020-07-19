#!/usr/bin/env python
# coding: utf-8

# In[32]:


import requests
from bs4 import BeautifulSoup
import json
import os


# In[33]:


url= "http://nek.istanbul.edu.tr:4444/ekos/GAZETE/"
r = requests.get(url)
soup = BeautifulSoup(r.content,"html.parser")
divs = soup.findAll("div", {"class": "col-6 col-sm-6 col-md-4 mb-4 mb-lg-0 col-lg-2"})


# In[34]:


def createDirectory(dirPath):
    if not os.path.isdir(dirPath):
        os.mkdir(dirPath)


# In[46]:


def write_to_text(paper_json,paper_name):
    dirPath = './Papers'
    filePath = '{}/{}.txt'.format(dirPath,paper_name)
    createDirectory(dirPath)
    with open(filePath, 'w') as f:
        json.dump(paper_json, f)
    print(filePath)


# In[47]:


def paper_to_json(paper,paper_name):
    paper_json_array = []
    tables = paper.findAll("div", {"class":"content"})
    for table in tables:#gazetenin yılları
        table_body = table.find('table')
        rows = table_body.find_all('tr')
        del rows[0] #tablonun sütun adları silinir
        for row in rows:#pdfs
            date = row.find('td').text
            url = row.find('a')['href']
            paper_json = {}
            #paper_json['name'] = paper_name
            paper_json['date'] = date
            paper_json['url'] = url
            paper_json_array.append(paper_json)
    write_to_text(paper_json_array,paper_name)


# In[48]:


for div in divs:#tüm gazeteler
    sub_url = div.find('a')['href']
    papers_url = url+sub_url
    r = requests.get(papers_url)
    paper = BeautifulSoup(r.content,"html.parser")
    paper_name = str(papers_url).split("=")[1]
    paper_to_json(paper,paper_name)


# In[ ]:


len(divs)


# In[ ]:




