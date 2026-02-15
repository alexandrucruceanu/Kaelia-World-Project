import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cont in data['continents']:
    for country in cont.get('countries', []):
        if 'cities' not in country:
            print(f"Error: Country '{country['name']}' in continent '{cont['name']}' is missing 'cities' array.")
        elif not isinstance(country['cities'], list):
            print(f"Error: Country '{country['name']}' in continent '{cont['name']}' has search 'cities' that is not a list.")
        else:
            for city in country['cities']:
                if 'coords' not in city:
                    print(f"Error: City '{city.get('name')}' in country '{country['name']}' is missing 'coords'.")
                if 'type' not in city:
                    print(f"Error: City '{city.get('name')}' in country '{country['name']}' is missing 'type'.")

print("Check complete.")
