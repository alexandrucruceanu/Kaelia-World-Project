import json
import os
import struct
import numpy as np
from PIL import Image

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MDR_FILE = os.path.join(BASE_DIR, '01_Design_Sources', 'Kaelia Equirectangular.mdr')
DATA_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'master_world_data.json')
LOOKUP_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'political_lookup.json')
MASK_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'political_mask.png')

# MDR Specs
HEADER_SIZE = 1024
WIDTH = 8192
HEIGHT = 4096

# Mapping from Country to Continent (based on WORLD_CODEX.md)
COUNTRY_TO_CONTINENT = {
    "Aghaz": "The Mirelands",
    "Akasy": "Kasy Federation",
    "Ax Pelak Yeldo": "The Mirelands",
    "Bakausy": "Kasy Federation",
    "Betereko": "Betereko",
    "Brechar": "Nordica",
    "Dirka'Merik": "Antarmund",
    "Fyny'Dor": "Antarmund",
    "Gryning": "Nordica",
    "Guldhorn": "Antarmund",
    "Kasim'Merik": "Antarmund",
    "Keunmor": "Nordica",
    "Kornmor": "Nordica",
    "Laendamania": "Antarmund",
    "Meit'Val": "Antarmund",
    "Melynmania": "Antarmund",
    "Menulys": "The Mirelands",
    "Mesek": "The Mirelands",
    "Metsemania": "Antarmund",
    "Misyats": "The Mirelands",
    "Nechars": "The Mirelands",
    "Niruz": "The Mirelands",
    "NorKunta": "Antarmund",
    "Norgborg": "Antarmund",
    "Norginde": "Antarmund",
    "Norgkes": "Antarmund",
    "Oighear": "Nordica",
    "Pateraz": "The Mirelands",
    "Pomkasy": "Kasy Federation",
    "Redez": "The Mirelands",
    "Saskasy": "Kasy Federation",
    "Sigmarignen": "Antarmund",
    "Tailaz": "The Mirelands",
    "Varelmond": "Antarmund",
    "Vorkasy": "Kasy Federation",
    "Yokasy": "Kasy Federation"
}

def main():
    if not all(os.path.exists(p) for p in [MDR_FILE, DATA_FILE, LOOKUP_FILE, MASK_FILE]):
        print("Required files missing.")
        return

    print("Loading data...")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        world_data = json.load(f)
    with open(LOOKUP_FILE, 'r', encoding='utf-8') as f:
        political_lookup = json.load(f)
    
    # Load MDR
    with open(MDR_FILE, 'rb') as f:
        f.seek(HEADER_SIZE)
        elevations = np.frombuffer(f.read(), dtype='<f4').reshape((HEIGHT, WIDTH))
    
    # Load Mask
    mask_img = Image.open(MASK_FILE).convert('RGB')
    mask_data = np.array(mask_img)
    mask_h, mask_w, _ = mask_data.shape

    # Helper: Get area pixels for a country
    def get_country_area(rgb_str):
        target_rgb = list(map(int, rgb_str.split(',')))
        # Efficiently find pixels
        mask = (mask_data[:, :, 0] == target_rgb[0]) & \
               (mask_data[:, :, 1] == target_rgb[1]) & \
               (mask_data[:, :, 2] == target_rgb[2])
        return np.argwhere(mask)

    # Countries already in JSON
    json_countries = {}
    for cont in world_data['continents']:
        for country in cont['countries']:
            json_countries[country['name']] = country

    added_cities = 0
    added_countries = 0

    # Iterate over all countries in lookup
    for rgb_str, info in political_lookup.items():
        country_name = info['country']
        continent_name = COUNTRY_TO_CONTINENT.get(country_name, info.get('continent', 'Unknown'))
        
        if continent_name == "Unknown":
            print(f"Skipping {country_name}: Continent unknown.")
            continue

        # Find or create country in JSON
        target_continent = next((c for c in world_data['continents'] if c['name'] == continent_name), None)
        if not target_continent:
            print(f"Creating continent: {continent_name}")
            target_continent = {"name": continent_name, "countries": []}
            world_data['continents'].append(target_continent)
        
        target_country = next((c for c in target_continent['countries'] if c['name'] == country_name), None)
        if not target_country:
            print(f"Creating country: {country_name}")
            target_country = {"name": country_name, "cities": []}
            target_continent['countries'].append(target_country)
            added_countries += 1

        # Check if country has cities
        if not target_country['cities']:
            print(f"Country {country_name} has no cities. Finding land...")
            pixels = get_country_area(rgb_str)
            if len(pixels) == 0:
                print(f"  !! No pixels found for color {rgb_str}")
                continue
            
            # Find a pixel area with elevation > 0
            found_land = False
            # Shuffle or sample to avoid always picking the top-left
            sample_idx = np.random.permutation(len(pixels))
            for idx in sample_idx:
                py_mask, px_mask = pixels[idx]
                
                # Rescale to MDR dimensions
                px_mdr = int(px_mask * WIDTH / mask_w)
                py_mdr = int(py_mask * HEIGHT / mask_h)
                
                # Check elevation
                elev = elevations[py_mdr, px_mdr]
                if elev > 0:
                    # Convert to Lat/Lng (0-1000, 0-2000)
                    lat = round(1000.0 * (1.0 - (py_mdr / HEIGHT)), 2)
                    lng = round(2000.0 * (px_mdr / WIDTH), 2)
                    
                    # Create city
                    city_id = f"city_auto_{len(target_country['cities']) + 1}_{country_name.lower().replace(' ', '_')}"
                    new_city = {
                        "id": city_id,
                        "name": f"{country_name} Capital",
                        "type": "metropolis",
                        "coords": [lat, lng],
                        "altitude": f"{int(round(elev))}m",
                        "population": "500,000",
                        "desc": f"The primary capital and economic hub of {country_name}.",
                        "heraldry": {
                            "motto": "Prosperity and Peace",
                            "description": f"Standardized heraldry for {country_name}."
                        }
                    }
                    target_country['cities'].append(new_city)
                    added_cities += 1
                    found_land = True
                    print(f"  -> Created city at ({lat}, {lng}) with elev {elev:.0f}m")
                    break
            
            if not found_land:
                print(f"  !! No land found for {country_name} (Underwater country?)")

    # Save
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(world_data, f, indent=2)
    
    print(f"\nDone. Added {added_countries} countries and {added_cities} cities.")

if __name__ == "__main__":
    main()
