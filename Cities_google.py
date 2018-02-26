import csv
import math
from geocoder import google

# Google geocoder API Key = AIzaSyD-RwSmbni2qUkCPK1xVyMZvzIXf40iqA4
api_key = 'AIzaSyD-RwSmbni2qUkCPK1xVyMZvzIXf40iqA4'


# Using Google geocoder API

def get_input():
    global place1, place2
    place1 = input('Where is the first place? ')
    place2 = input('Where is the second place? ')


def get_coordinates(search_term):
    return google(search_term, key=api_key).latlng


def get_unit():
    while True:
        unit = input('Miles or kilometers? ').upper()
        if unit == 'MILES' or unit == 'M':
            unit = 'M'
            return unit
        elif unit == 'KILOMETERS' or unit == 'KM':
            unit = 'KM'
            return unit
        else:
            print('Please choose miles or kilometers')
            continue


def calc_dist(coord1, coord2):
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    unit = get_unit()

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    dist = round(6367 * c, 3)
    if unit == 'M':
        dist *= 0.621371
    print(dist)

place1 = ''
place2 = ''

while True:
    get_input()
    place1_coord = get_coordinates(place1)
    place2_coord = get_coordinates(place2)
    calc_dist(place1_coord,place2_coord)
    if input('Do you want another measurement? (Y/N) ').upper().startswith('Y'):
        continue
    else:
        break
