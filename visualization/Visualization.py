
# coding: utf-8

# In[290]:


from flask import Flask
from flask_cors import CORS
from flask import jsonify
from threading import Thread
from flask import render_template
from flask import request
import folium
import json


# In[291]:


_map = folium.Map(location=[38.9597594, 34.9249653],zoom_start=7,tiles="Mapbox Control Room")


# In[292]:


cityBoundaries = folium.FeatureGroup(name="City Boundaries")


# In[293]:


cityBoundaries.add_child(folium.GeoJson(open("cities.json","r",encoding="utf-8-sig").read(),
                                     style_function=lambda city: {'fillColor':"red"}))


# In[294]:


_map.add_child(cityBoundaries)
_map.add_child(folium.LayerControl())


# In[310]:


def show_on_map(_map,word,year):
    cities = open("cities_of_turkey.json","r+").read()
    cities = json.loads(cities)
    for city in cities:
        point = [city['latitude'],city['longitude']]
        name = city['name']
        folium.Marker(point,popup=[word,year,name],tooltip='Click For Date Information').add_to(_map)
    cityBoundaries = folium.FeatureGroup(name="City Boundaries")
    _map.save("turkey.html")


# In[311]:


def start_service():
    global _map
    keyword = "Nothing"
    year = 0
    app = Flask(__name__)
    
    CORS(app)
    
    @app.route('/main', methods=['GET'])
    def get():
        keyword = request.args.get('word', None)
        year = request.args.get('year', None)
        print(keyword,year)
        if keyword and year:
            show_on_map(_map,keyword,year)
        return open("main.html","r+").read()
        
    @app.route('/map',methods=['GET'])
    def get_map():
        return open("turkey.html","r+").read()
    
    @app.route('/text',methods=['GET'])
    def get_text():
        return open("text.html","r+").read()
    
#     @app.route('/input',methods=['GET'])
#     def get_input():
#         return open("input.html","r+").read()
    
    app.run(host='0.0.0.0', port=5000)


# In[312]:


start_service()


# In[166]:


thread = Thread(target=start_service)


# In[ ]:


thread.start()

