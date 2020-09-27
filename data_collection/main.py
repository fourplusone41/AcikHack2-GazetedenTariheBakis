#!/usr/bin/env python
# coding: utf-8

import os
import json
import time
import pickle
import requests
import configparser
#from queue import Queue
#from threading import Thread
from multiprocessing import Lock
from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool

from tqdm import tqdm
from bs4 import BeautifulSoup

from db_handler import DB_Handler
from ocr_handler import OCR_Handler
from ner_handler import NER_Handler
from elk_handler import ELK_Handler
#from solr_handler import Solr_Handler

config = configparser.ConfigParser()
config.read('settings.ini')
DATASET_URL = config["DEFAULT"]["dataset_url"]

db_gazete = DB_Handler("gazete")
db_page = DB_Handler("page")
ner = NER_Handler()
#solr = Solr_Handler()
es = ELK_Handler()

# multithreading
lock = Lock()
issues = []

# Queue for multithreading
#row_queue = Queue()

# List for no multithreading
# row_list = []

def createDirectory(dirPath):
    if not os.path.isdir(dirPath):
        os.mkdir(dirPath)

def write_to_text(paper_json,paper_name):
    dirPath = './Papers'
    filePath = '{}/{}.txt'.format(dirPath,paper_name)
    createDirectory(dirPath)
    with open(filePath, 'w') as f:
        json.dump(paper_json, f)
    print(filePath)

def date_formatter(date):
    date_modern = date
    date_table = {
        "ikinci kanun": "01",
        "Kanunu Sani": "01",
        "şubat": "02",
        "mart": "03",
        "nisan": "04",
        "mayıs": "05",
        "haziran": "06",
        "temmuz": "07",
        "ağustos": "08",
        "eylül": "09",
        "birinci teşrin": "10",
        "teşrin-i evvel": "10",
        "ikinci teşrin": "11",
        "teşrin-i sani": "11",
        "birinci kanun": "12",
        "kanunu rvvel": "12"
    }
    for k,v in date_table.items():
        date_modern = date_modern.lower().replace(k, v)

    date_return = date_modern.split(" ")
    date_return.reverse()
    return "_".join(date_return)

# def parallel_process():
#     while True:
#         row = row_queue.get()
#         date = date_formatter(row.find('td').text)
#         url = row.find('a')['href']
#         pdf = paper_download(url)
#         paper_json = {}
#         paper_json['name'] = paper_name
#         paper_json['date'] = date
#         paper_json['url'] = url
#         db_gazete.save(paper_json, pdf, "application/pdf")
#         # es.index(paper_json, "gazete-index")
        
#         ocr = OCR_Handler(pdf)
#         ocr.run()
#         for i, text in enumerate(ocr.text):
#             paper_json["ner"] = ner.run(text)
#             paper_json["page"] = i + 1
#             paper_json["text"] = text
#             img_tmp = ocr.pages[i]
#             #INFO: Solr replaced with elasticsearch
#             es.index(paper_json, "page-index")
#             db_page.save(paper_json, img_tmp, "image/png")
            

#         row_queue.task_done()

# def process(row):
#     date = date_formatter(row.find('td').text)
#     url = row.find('a')['href']
#     try:
#         pdf = paper_download(url)
#     except:
#         print("Error downloading {}".format(url))
#     else:
#         paper_json = {}
#         paper_json['name'] = paper_name
#         paper_json['date'] = date
#         paper_json['url'] = url
#         db_gazete.save(paper_json, pdf, "application/pdf")
#         # es.index(paper_json, "gazete-index")

#         # ocr = OCR_Handler(pdf)
#         # ocr.run()
#         # for i, text in enumerate(ocr.text):
#         #     paper_json["ner"] = ner.run(text)
#         #     paper_json["page"] = i + 1
#         #     paper_json["text"] = text
#         #     img_tmp = ocr.pages[i]
#         #     #INFO: Solr replaced with elasticsearch
#         #     es.index(paper_json, "page-index")
#         #     db_page.save(paper_json, img_tmp, "image/png")




# def paper_to_db(paper,paper_name):    
#     row_list = []
#     tables = paper.findAll("div", {"class":"content"})
#     print("## Processing " + paper_name)
    
#     #workers = [
#     #    Thread(target=parallel_process, daemon=True)
#     #    for _ in range(1)
#     #]

#     for table in tables: #gazetenin yılları
#         table_body = table.find('table')
#         rows = table_body.find_all('tr')
#         del rows[0] #tablonun sütun adları silinir
#         for row in rows: #pdfs
#             #row_queue.put(row)
#             process(row)

#     #print("#### Running jobs for " + paper_name)
#     #for w in workers:
#     #    w.start()

#     #for w in tqdm(workers):
#     #    w.join()

def download_size(issue):
    row = issue[0]
    url = row.find('a')['href']
    try:
        r = requests.get(url, stream=True).headers['Content-length']
        return r
    except:
        return 0

def download(issue_nmbr):
    issue = issues[issue_nmbr]
    row = issue[0]
    paper_name = issue[1]

    date = date_formatter(row.find('td').text)
    url = row.find('a')['href']
    try:
        r = requests.get(url)
        pdf = r.content
    except:
        return(url)

    paper_json = {}
    paper_json['name'] = paper_name
    paper_json['date'] = date
    paper_json['url'] = url
    db_gazete.save(paper_json, pdf, "application/pdf")
    return True

def scrap():
    r = requests.get(DATASET_URL)
    soup = BeautifulSoup(r.content,"html.parser")
    divs = soup.findAll("div", {"class": "col-6 col-sm-6 col-md-4 mb-4 mb-lg-0 col-lg-2"})

    papers = []
    for div in tqdm(divs): #tüm gazeteler
        sub_url = div.find('a')['href']
        papers_url = DATASET_URL+sub_url
        r = requests.get(papers_url)
        paper = BeautifulSoup(r.content,"html.parser")
        paper_name = str(papers_url).split("=")[1]
        papers.append((paper,paper_name))

    issues = []
    for paper, paper_name in tqdm(papers):
        tables = paper.findAll("div", {"class":"content"})
        for table in tables: #gazetenin yılları
            table_body = table.find('table')
            rows = table_body.find_all('tr')
            del rows[0] #tablonun sütun adları silinir
            for row in rows: #pdfs
                issues.append((row, paper_name))

    print("# Downloading {} Total Issues from {} Papers #".format(len(issues), len(papers)))

    return issues
    
if __name__ == '__main__':
    
    issues = scrap()
    nmbr_issues = len(issues)

    # sizes = []
    # for issue in tqdm(issues):
    #     ret = download_size(issue)
    #     sizes.append(ret)

    # print("# Downloading {} Bytes of data! {} Links failed.".format(sum(sizes), len([x for x in sizes if x == 0])))

    # downloads = []
    # for issue in tqdm(issues):
    #     ret = download(issue)
    #     downloads.append(ret)

    # https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar/
    # https://stackoverflow.com/questions/52021254/maximum-recursion-depth-exceeded-multiprocessing-and-bs4
    
    # pool = Pool(os.cpu_count())
    # downloads = list(tqdm(pool.imap(download, range(nmbr_issues)), total=nmbr_issues))
    downloads = []
    with Pool(os.cpu_count()) as pool:
        with tqdm(total=nmbr_issues) as pbar:
            for j, d in enumerate(pool.imap(download, range(nmbr_issues))):
                downloads.append(d)
                pbar.update()
    
    # fails = [x for x in downloads if x is not True]
    # print("# Successful: {} | Failed: {}".format(len(downloads) - len(fails), len(fails)))
    # with open("fails.txt", "w") as f:
    #     f.write(json.dumps(fails))

    #paper_to_db(paper,paper_name)