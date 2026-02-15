import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids = {}
for cont in data['continents']:
    for country in cont.get('countries', []):
        for city in country.get('cities', []):
            city_id = city.get('id')
            if city_id in ids:
                print(f"Duplicate City ID: '{city_id}' (City: '{city['name']}', previously seen in '{ids[city_id]}')")
            ids[city_id] = city['name']

print("Global ID check complete.")
