import json
from math import sqrt
import webbrowser
from lib import tsp_solver
import folium

if __name__ == '__main__':
    with open('Data/20_cities_GER.json', 'r') as f:
        city_data_json = json.load(f)

    city_data = {}
    for city in city_data_json:
        city_data[city['city']] = (float(city['lat']), float(city['lng']))

    def calc_distance_of_two_cities(city1, city2):
         return sqrt((city2[0] - city1[0])**2 + (city2[1] - city1[1])**2)
        
    city_distances = {}
    for city in city_data.keys():
        for connecting_city in city_data.keys():
            if city == connecting_city:
                continue
            city_distances[(city, connecting_city)] = calc_distance_of_two_cities(city_data[city], city_data[connecting_city])
            
            
    shortes_route = tsp_solver.solve_tsp(city_distances,city_data.keys())
    
    def plot_route(city_data, route):
        m = folium.Map(location=city_data[route[0][0]], zoom_start=6)

        for city, coordinates in city_data.items():
            folium.Marker(location=coordinates, popup=city).add_to(m)

        route_coordinates = [city_data[city[0]] for city in route]
        route_coordinates.append(route_coordinates[0])
        folium.PolyLine(route_coordinates, color="red", weight=2.5, opacity=1).add_to(m)
        return m
    
    map = plot_route(city_data, shortes_route)
    map.save('route_map.html')
    webbrowser.open('route_map.html')
    
    print('Done...')