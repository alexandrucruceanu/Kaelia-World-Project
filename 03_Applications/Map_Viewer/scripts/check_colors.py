import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cont in data['continents']:
    if cont['name'] == "Antarmund":
        for country in cont.get('countries', []):
            for city in country.get('cities', []):
                color = city.get('color')
                if not color:
                    print(f"Error: City '{city['name']}' in Antarmund is missing color.")
                elif not color.startswith('#'):
                    print(f"Error: City '{city['name']}' has invalid color format: '{color}'")

print("Color check complete.")
