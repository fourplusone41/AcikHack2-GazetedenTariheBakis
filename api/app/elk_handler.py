import os
import configparser
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Date, DateRange

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
        self.client = Elasticsearch(['http://elastic:changeme@localhost:9200/'])

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

        res = self.client.index(index=es_index, id=doc_id, body=data)
        print(res['result'])

    def query(self, keyword, start_date, end_date):

        sdate_ = [int(x) for x in start_date.split('_')]
        edate_ = [int(x) for x in end_date.split('_')]

        s = Search(using=self.client, index="page-index") \
            .filter("range", timestamp={'gte': datetime(sdate_[0], sdate_[1], sdate_[2]), 'lt': datetime(edate_[0], edate_[1], edate_[2])},) \
            .query("multi_match", query=keyword, fields=['text', 'ner.PERSON', 'ner.LOCATION', 'ner.ORGANIZATION']) \
            #.filter("range", **{'@timestamp': {'gte': start_date.replace('_', '-') , 'lt': end_date.replace('_', '-'), }}) \
            #.filter("term", date="1936_07_01") \
            #.query("match", text="ankara")   \
            #.exclude("match", description="beta")

        response = s.execute()

        res = []

        for hit in s:
            res.append(hit.to_dict())
            print(hit.title)

        return res #s.to_dict()



