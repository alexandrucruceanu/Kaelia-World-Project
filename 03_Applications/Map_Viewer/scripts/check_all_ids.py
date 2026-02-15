import json

with open('g:/Mi unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/data/master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids = {}
def check(obj, path):
    oid = obj.get('id')
    if oid:
        if oid in ids:
            print(f"Duplicate ID: '{oid}' at {path} (previously seen at {ids[oid]})")
        ids[oid] = path

for cont in data['continents']:
    check(cont, f"Continent: {cont['name']}")
    for country in cont.get('countries', []):
        check(country, f"Country: {country['name']}")
        for city in country.get('cities', []):
            check(city, f"City: {city['name']}")

print("Full ID check complete.")
