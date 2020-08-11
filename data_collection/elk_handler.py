import os
import configparser
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search



#Solr baglantisi
config = configparser.ConfigParser()
config.read('settings.ini')

URL = config["ELK"]["es_server"]
UN = config["ELK"]["es_un"]
PW = config["ELK"]["es_pw"]


class ELK_Handler():
    """
    ELK handler
    """
    def __init__(self):
        self.es = Elasticsearch(['http://elastic:changeme@localhost:9200/'])

    def index(self, data, es_index):
        doc_id = ""
        if (es_index == "gazete-index"):
            doc_id = ".".join((data["date"], data["name"]))
        elif (es_index == "page-index"):
            doc_id = ".".join((data["date"], data["name"] + "_" + str(data["page"])))
        data["id"] = doc_id
        data["title"] = doc_id

        try:
            del data["_id"] # _id is not allowed
        except:
            pass

        date_ = [int(x) for x in data["date"].split('_')]
        data['timestamp'] = datetime(date_[0], date_[1], date_[2])

        res = self.es.index(index=es_index, id=doc_id, body=data)
        print(res['result'])
