import io
import os
import configparser
from cloudant.client import CouchDB
from cloudant.document import Document
from cloudant.result import Result, ResultByKey

#veritabani baglantisi
config = configparser.ConfigParser()
config.read('settings.ini')

USERNAME = config["DB"]["db_username"]
PASSWORD = config["DB"]["db_password"]
URL = config["DB"]["db_server"]


class DB_Handler():
    """
    CouchDB handler
    """
    def __init__(self, db_name):
        self.client = CouchDB(USERNAME, PASSWORD, url= URL, connect=True)
        self.db_name = db_name
        self.db = None
        try:
            self.db = self.client.create_database(self.db_name)
        except:
            self.db = self.client[self.db_name]

    def save(self, data, attachment = None, att_type = None):
        doc_id = ""
        if (self.db_name == "gazete"):
            doc_id = ".".join((data["date"], data["name"]))
        elif (self.db_name == "page" or self.db_name == "page_txt"):
            doc_id = ".".join((data["date"], data["name"] + "_" + str(data["page"])))
        data["_id"] = doc_id

        try:
            del data['timestamp'] # timestamps are not allowed
        except:
            pass
        
        self.db.create_document(data)
        if attachment:
            if (att_type == "image/png"):
                buf = io.BytesIO()
                attachment.save(buf, format='JPEG')
                attachment = buf.getvalue()
            with Document(self.db, doc_id) as document:
                document.put_attachment(att_type.split("/")[-1], att_type, attachment)
    
    def get_doc(self, doc_id):
        #doc = self.db[doc_id]
        doc = None
        att = None
        with Document(self.db, doc_id) as document:
            doc = document
            att = document.get_attachment("png")
        return doc, att

    def update_doc(self, doc_id, new_data):
        with Document(self.db, doc_id) as document:
            for k in new_data.keys():
                document[k] = new_data[k]

    def del_doc(self, doc_id):
        document = self.db[doc_id]
        document.delete()

    def query_id(self,  id_value):
        selector = {'_id': {'$eq': id_value}}
        docs = self.db.get_query_result(selector)
        
    def query_all(self, start = 0, end = 100):
        ids = []
        result_collection = Result(self.db.all_docs)
        result = result_collection[start:end]
        for res in result:
            ids.append(res['id'])

        return ids


            
        

