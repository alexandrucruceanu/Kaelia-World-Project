import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cont in data['continents']:
    for country in cont.get('countries', []):
        for city in country.get('cities', []):
            coords = city.get('coords')
            if not isinstance(coords, list) or len(coords) != 2:
                print(f"Error: City '{city.get('name')}' in country '{country['name']}' has invalid coords: {coords}")
            elif not all(isinstance(x, (int, float)) for x in coords):
                 print(f"Error: City '{city.get('name')}' in country '{country['name']}' has non-numeric coords: {coords}")

print("Deep Coords check complete.")
