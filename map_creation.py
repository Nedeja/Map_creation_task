import geopy
import geopy.distance
import folium
import time
from geopy.geocoders import Nominatim


year = input('Enter a year you would like to have a map for:')
current_location = input('Enter your current location(format: lat, long):')
current_location = current_location.split(', ')
current_location = tuple([float(x) for x in current_location])
# print(current_location)

path = 'locations1.list'
def open_file(path):
    """
    (str) -> (list)
    this function opens a file from which we read 
    needed information
    >>> open_file('locations1.list)
    [['"#1', 'Single"', '(2006)', 'Los', 'Angeles,', 'California,', 'USA'], 
    ['"#1', 'Single"', '(2006)', 'New', 'York', 'City,', 'New', 'York,', 'USA'], 
    ['"#15SecondScare"', '(2015)', 'Coventry,', 'West', 'Midlands,', 'England,', 'UK'], 
    ['"#15SecondScare"', '(2015)', 'West', 'Hills,', 'California,', 'USA'], 
    ['"#15SecondScare"', '(2015)', 'West', 'Hills,', 'California,', 'USA']]...
    """
    lst = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        line = f.readline()
        while not line.startswith("=============="):
            line = f.readline()
        for line in f:
            if '{' in line:
                ind_start, ind_last = line.find('{'), line.find('}')
                line = line[:ind_start- 1] + line[ind_last + 1:]
            ind = line[::-1].find('(')
            if line.find("(") != len(line) - ind - 1:
                line = line[:len(line) - ind - 1]
            lst.append(line.strip().split())
    return lst
film_list = open_file(path)
print(film_list)

def finding_year_films(film_list, year):
    """
    (list, str) -> (list)
    this function creates a list of films that were casted in the
    year user wants to have
    """
    year_list = []
    year = "(" + year + ")"
    for i in film_list:
        if year in i:
            year_list.append(i)
    year_list_joined = []
    for j in year_list:
        for l in j:
            if '}' in l:
                ind1 = j.index(l)
                year_list_joined.append((j[:ind1 + 1], n))
            elif ')' in l:
                ind2 = j.index(l)
                n = j[:ind2 + 1] + [" ".join(j[ind2 + 1:])]
                year_list_joined.append(n)
    return year_list_joined
year_list_joined = finding_year_films(film_list, year)
# print(finding_year_films(film_list, year))

def create_location(year_list_joined):
    """
    (list) -> (list)
    this function creates a list of films and thaeir locations
    as latitude and longtitude
    """
    geolocator = Nominatim(user_agent="main.py")
    location_lst = []
    for i in year_list_joined:
        location = geolocator.geocode(i[-1])
        location_lst.append((i[0], (location.latitude, location.longitude)))
    return location_lst
location_lst = create_location(year_list_joined)
# print(create_location(year_list_joined))

def find_nearest_ten(location_lst, current_location):
    """
    (list, str) -> (list)
    this function finds the nearest ten films to the location
    that was entered by user
    """
    len_list = []
    for i in location_lst:
        length = str(geopy.distance.geodesic(current_location, i[-1]))
        length = length.replace(' km', '')
        len_list.append((i[0], float(length), i[-1]))
    len_list = sorted(len_list, key = lambda x: x[1])
    return len_list[:9]
len_list = find_nearest_ten(location_lst, current_location)
# print(find_nearest_ten(location_lst, current_location))

m = folium.Map(location=list(current_location), zoom_start=11)
first_layer = folium.FeatureGroup(name='My current location')
first_layer.add_child(folium.Marker(list(current_location), popup='my_point', tooltip=1))
second_layer = folium.FeatureGroup(name='Films near me')
for i in len_list:
    second_layer.add_child(folium.Marker(list(i[-1]), popup=i[0], tooltip=1))
third_layer = folium.FeatureGroup(name='Five highest mountains')
third_layer.add_child(folium.Marker([27.988056, 86.925278], popup='Everest', tooltip=1))
third_layer.add_child(folium.Marker([35.881389, 76.513333], popup='K2', tooltip=1))
third_layer.add_child(folium.Marker([27.703333, 88.1475], popup='Kangchenjunga', tooltip=1))
third_layer.add_child(folium.Marker([27.961667, 86.933056], popup='Lhotse', tooltip=1))
third_layer.add_child(folium.Marker([27.889722, 87.088889], popup='Makalu', tooltip=1))
m.add_child(first_layer)
m.add_child(second_layer)
m.add_child(third_layer)
m.add_child(folium.LayerControl())
m.save("map.html")