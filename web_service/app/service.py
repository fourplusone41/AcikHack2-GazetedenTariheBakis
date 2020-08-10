
# coding: utf-8

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from utils import *

keyword = "Nothing"
year = 0
app  = Flask(__name__)
CORS(app)

@app.route('/main', methods=['GET'])
def get():
    _map = create_map()
    keyword = request.args.get('word', None)
    year = request.args.get('year', None)
    print(keyword,year)
    if keyword and year:
        text,locations = show_on_text()
        crete_text_html(text)
        show_on_map(_map,locations,keyword,year)
    else:
        crete_text_html("<h1>NewsPapers List</h1>")
        _map.save("turkey.html")
    return open("main.html","r+",encoding="utf-8-sig").read()
    
@app.route('/map',methods=['GET'])
def get_map():
    return open("turkey.html","r+",encoding="utf-8-sig").read()

@app.route('/text',methods=['GET'])
def get_text():
    return open("text.html","r+",encoding="utf-8-sig").read()

@app.route('/newspaper',methods=['GET'])
def get_newspaper():
#         return open("newspaper.html","r+",encoding="utf-8-sig").read()
        return "Merhaba Rumed"

app.run(host='0.0.0.0', port=5000)
