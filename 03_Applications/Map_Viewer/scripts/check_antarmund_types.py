import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

layers = ["capital", "metropolis", "settlement", "village", "special"]
found_types = set()

for cont in data['continents']:
    if cont['name'] == "Antarmund":
        for country in cont.get('countries', []):
            for city in country.get('cities', []):
                ctype = city.get('type')
                found_types.add(ctype)
                if ctype not in layers:
                    print(f"Error: City '{city['name']}' in Antarmund has UNKNOWN type: '{ctype}'")

print(f"Found types in Antarmund: {found_types}")
