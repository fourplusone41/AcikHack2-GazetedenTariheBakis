import io
import os
import configparser
from cloudant.client import CouchDB
from cloudant.document import Document


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
        print("connecting to DB: " + URL)
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
        elif (self.db_name == "page"):
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

    def query(self, id):
        selector = {'_id': {'$eq': id}}
        docs = self.db.get_query_result(selector)
        for doc in docs:
            print(doc)

    # def query_attachement(self, id):
    #     selector = {'_id': {'$eq': id}}
    #     docs = self.db.get_attachement()
    #     for doc in docs:
    #         print(doc)

            
        

