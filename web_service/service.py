
# coding: utf-8

import json
import requests
from threading import Thread

import folium
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

def create_map():
    _map = folium.Map(location=[38.9597594, 34.9249653],zoom_start=6,tiles="Mapbox Control Room")
    cityBoundaries = folium.FeatureGroup(name="City Boundaries")
    cityBoundaries.add_child(folium.GeoJson(open("cities.json","r",encoding="utf-8-sig").read(),
                                     style_function=lambda city: {'fillColor':"red"}))
    _map.add_child(cityBoundaries)
    _map.add_child(folium.LayerControl())
    _map.save("turkey.html")
    return _map

def show_on_map(_map,locations,word,year):
    cities = open("cities_of_turkey.json","r+",encoding="utf-8-sig").read()
    cities = json.loads(cities)
    for city in cities:
        point = [city['latitude'],city['longitude']]
        name = city['name']
        if name in locations:
            folium.Marker(point,popup=[word,year,name],tooltip='Click For More Information').add_to(_map)
    _map.save("turkey.html")

def convert_to_table(newspapers):
    styles = open("table.css","r+",encoding="utf-8-sig").read()
    table = "<table border=1 id='customers'><tr>"
    for key in newspapers['newspapers'][0].keys():
        table += "<th>"+key+"</th>"
    table +="<tr>"
    for newspaper in newspapers['newspapers']:
        table +="<tr>"
        counter = 0
        for value in newspaper.values():
            if counter == 2:
                name = "Gazete"
                table += "<td>"+' <a href="{}" target="_blank">{}</a></td>'.format(str(value),name)
            else:
                table += "<td>{}</td>".format(str(value))
            counter += 1
        table +="</tr>"
    table += "</table>"
    return styles+table


def show_on_text():
    url = "APİ_URL"
    headers = {'Content-type': 'application/json'}
    r = requests.get(url,headers=headers)
    data_str = r.text.replace("'", '"')
    data_json = json.loads(data_str)
    locations = []
    for newspaper in data_json['newspapers']:
        locations.append(newspaper['location'])
    return convert_to_table(data_json),locations


def crete_text_html(text):
    text_html= open("text.html","w",encoding="utf-8-sig")
    text_html.write(text)
    text_html.close()


def start_service():
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

start_service()
thread = Thread(target=start_service)
thread.start()
