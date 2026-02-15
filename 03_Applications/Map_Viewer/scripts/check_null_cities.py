import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cont_idx, cont in enumerate(data['continents']):
    for country_idx, country in enumerate(cont.get('countries', [])):
        if country.get('cities') is None:
             print(f"Error: Country '{country['name']}' in continent '{cont['name']}' has cities=null")
        elif not isinstance(country['cities'], list):
             print(f"Error: Country '{country['name']}' in continent '{cont['name']}' has cities of type {type(country['cities'])}")

print("Null cities check complete.")
