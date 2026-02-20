
import json
import os

DATA_FILE = r"c:\Proyectos_Local\Software-Development\Simulations\World_Building_Project\03_Applications\Map_Viewer\data\master_world_data.json"

def move_city(city_name, target_country_name):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    city_obj = None
    source_country = None
    
    # Find and remove city
    for continent in data['continents']:
        for country in continent['countries']:
            for i, city in enumerate(country['cities']):
                if city['name'] == city_name:
                    city_obj = country['cities'].pop(i)
                    source_country = country['name']
                    print(f"Found {city_name} in {source_country}")
                    break
            if city_obj: break
        if city_obj: break

    if not city_obj:
        print(f"City {city_name} not found.")
        return

    # Find target country and add city
    target_found = False
    for continent in data['continents']:
        for country in continent['countries']:
            if country['name'] == target_country_name:
                # Update city data
                city_obj['countryName'] = target_country_name
                # Add to new country
                country['cities'].append(city_obj)
                target_found = True
                print(f"Moved {city_name} to {target_country_name}")
                break
        if target_found: break

    if not target_found:
        print(f"Target country {target_country_name} not found.")
        return

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    move_city("Kaldakinn", "Oighear")
