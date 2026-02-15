import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

layers = ["capital", "metropolis", "settlement", "village", "special"]

for cont in data['continents']:
    if cont['name'] == "Antarmund":
        for country in cont.get('countries', []):
            for city in country.get('cities', []):
                ctype = city.get('type')
                if ctype != ctype.strip():
                    print(f"Error: City '{city['name']}' has whitespace in type: '{ctype}'")
                if ctype not in layers:
                    print(f"Error: City '{city['name']}' has invalid type: '{ctype}'")

print("Whitespace check complete.")
