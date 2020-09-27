
# coding: utf-8

import json
import requests
from datetime import datetime

from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse

#from db_handler import DB_Handler
from elk_handler import ELK_Handler

keyword = "Nothing"
year = 0

app = Flask(__name__)
api = Api(app)

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('keyword', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)

#db_page = DB_Handler("page")
es = ELK_Handler()

class GazeteQuery(Resource):
    def get(self):
        args = parser.parse_args()

        res = es.query(args['keyword'], args['start_date'], args['end_date'])
        for i, _ in enumerate(res):
            res[i]['png'] = "http://localhost:5984/page/" + res[i]['id'] + "/png"

        return res

        # return {'hello': 'world',
        #         'keyword': args['keyword'],
        #         'start_date': args['start_date'],
        #         'end_date': args['end_date'] }

api.add_resource(GazeteQuery, '/query')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)

