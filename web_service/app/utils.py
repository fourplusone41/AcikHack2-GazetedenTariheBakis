import json
import requests
import folium

def create_map():
    _map = folium.Map(location=[38.9597594, 34.9249653],zoom_start=6,tiles="Mapbox Control Room")
    cityBoundaries = folium.FeatureGroup(name="City Boundaries")
    cityBoundaries.add_child(folium.GeoJson(open("cities.json","r",encoding="utf-8-sig").read(),
                                     style_function=lambda city: {'fillColor':"red"}))
    _map.add_child(cityBoundaries)
    _map.add_child(folium.LayerControl())
    _map.save("turkey.html")
    return _map

def show_on_map(_map,locations,keyword,year):
    cities = open("cities_of_turkey.json","r+",encoding="utf-8-sig").read()
    cities = json.loads(cities)
    for city in cities:
        point = [city['latitude'],city['longitude']]
        name = city['name']
        if name in locations:
            folium.Marker(point,popup=[keyword,year,name],tooltip='Click For More Information').add_to(_map)
    _map.save("turkey.html")

def convert_to_table(newspapers):
    styles = open("table.css","r+",encoding="utf-8-sig").read()
    table = "<table border=1 id='customers'><tr>"
    for key in ['name', 'date', 'page', 'png', 'text']:
        table += "<th>"+key+"</th>"
    table +="<tr>"
    for newspaper in newspapers:
        table +="<tr>"
        for key in ['name', 'date', 'page', 'png', 'text']:
            if (key == "png"):
                table += "<td><a href={} target=\"_blank\">{}</a></td>".format(str(newspaper[key]), str(newspaper[key]))
            else:
                table += "<td>{}</td>".format(str(newspaper[key]))
        table +="</tr>"
    table += "</table>"
    return styles+table


def show_on_text(url):
    print("### " + url)
    r = requests.get(url)
    data_json = r.json()
    locations = []
    for newspaper in data_json:
        for loc in newspaper['ner']['LOCATION']:
            locations.append(loc)
    return convert_to_table(data_json),locations


def crete_text_html(text):
    text_html= open("text.html","w",encoding="utf-8-sig")
    text_html.write(text)
    text_html.close()