import json
import os

data_path = 'data/master_world_data.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

norkunta = None
for cont in data['continents']:
    for country in cont['countries']:
        if country['name'] == 'NorKunta':
            norkunta = country
            break
    if norkunta: break

if norkunta:
    print(f"Country: {norkunta['name']}")
    print(f"  Flag: {norkunta['heraldry']['flag']}")
    print(f"  Arms: {norkunta['heraldry']['coat_of_arms']}")
    print(f"  Desc: {norkunta['heraldry']['description']}")
    print(f"  Motto: {norkunta['heraldry']['motto']}")
    print("-" * 20)
    for city in norkunta['cities']:
        print(f"City: {city['name']}")
        print(f"  Flag: {city['heraldry']['flag']}")
        print(f"  Arms: {city['heraldry']['coat_of_arms']}")
        print(f"  Desc: {city['heraldry']['description']}")
        print(f"  Motto: {city['heraldry']['motto']}")
        print("-" * 20)
else:
    print("NorKunta not found.")
