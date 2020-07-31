
# coding: utf-8

import json
import requests
from threading import Thread

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from cloudant.client import CouchDB
from cloudant.document import Document

import pysolr

def start_service():
    keyword = "Nothing"
    year = 0
    app  = Flask(__name__)
    CORS(app)
    
    @app.route('/query/<keyword>/<start_date>/<end_date>', methods=['GET'])
    def get_result():
        #TODO
        return 0
        
    app.run(host='0.0.0.0', port=4000)

start_service()
thread = Thread(target=start_service)
thread.start()
