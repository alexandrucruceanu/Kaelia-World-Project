import json

with open(r'g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\03_Applications\Map_Viewer\data\master_world_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_countries = 0
total_cities = 0

for continent in data['continents']:
    for country in continent['countries']:
        total_countries += 1
        total_cities += len(country.get('cities', []))

print(f"Total Countries: {total_countries}")
print(f"Total Cities: {total_cities}")
