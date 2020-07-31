import os
import configparser
import pysolr


#Solr baglantisi
config = configparser.ConfigParser()
config.read('settings.ini')

URL = config["SOLR"]["solr_server"]


class Solr_Handler():
    """
    Solr handler
    """
    def __init__(self):
        self.solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True)
        self.solr.ping()

    def index(self, data):
        doc_id = ".".join((data["date"], data["name"] + "_" + data["page"]))
        data["id"] = doc_id
        data["title"] = doc_id
        self.solr.add([data])