import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cont in data['continents']:
    for country in cont.get('countries', []):
        keys = country.keys()
        if 'cities' not in keys:
            print(f"Error: Country '{country['name']}' in continent '{cont['name']}' is missing 'cities' key. Keys: {list(keys)}")
        for k in keys:
            if k.lower() == 'cities' and k != 'cities':
                print(f"Error: Country '{country['name']}' has misspelled cities key: '{k}'")

print("Misspelled keys check complete.")
