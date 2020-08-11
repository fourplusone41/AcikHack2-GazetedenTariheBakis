
# coding: utf-8

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from utils import *

app  = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    _map = create_map()
    if request.method == 'POST':
        keyword = str(request.form['keyword'])
        start_year = str(request.form['start_year'])
        end_year = str(request.form['end_year'])
        
        print(keyword,start_year, end_year)
        if keyword and start_year and end_year:
            text,locations = show_on_text("http://localhost:4000/query?keyword={}&start_date={}_01_01&end_date={}_12_31".format(keyword, start_year, end_year))
            crete_text_html(text)
            #show_on_map(_map,locations,keyword,start_year)
        
        return render_template('results.html', page="Results")

    else:
        crete_text_html("<h1>NewsPapers List</h1>")
        #_map.save("turkey.html")
        return render_template('index.html', page="Home")

    
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

app.run(host='0.0.0.0', port=3000)
