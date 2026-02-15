import json
import math
import os
from PIL import Image

# Configuration
# Adjust paths to match where the script is run from (scripts folder -> ../data)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

MASTER_DATA_FILE = os.path.join(DATA_DIR, 'master_world_data.json')
LEGEND_DATA_FILE = os.path.join(DATA_DIR, 'climate_legend_data.json')
CLIMATE_MAP_FILE = os.path.join(DATA_DIR, 'climate_map.jpg')

MAP_LAT_MAX = 1000
MAP_LNG_MAX = 2000

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_pixel_coords(lat, lng, width, height):
    # App.js logic:
    # var yPct = 1 - (lat / 1000);
    # var xPct = lng / 2000;
    
    y_pct = 1 - (lat / MAP_LAT_MAX)
    x_pct = lng / MAP_LNG_MAX
    
    pixel_x = math.floor(x_pct * width)
    pixel_y = math.floor(y_pct * height)
    
    # Clamp
    pixel_x = max(0, min(pixel_x, width - 1))
    pixel_y = max(0, min(pixel_y, height - 1))
    
    return pixel_x, pixel_y

def get_closest_climate(rgb, legend):
    r, g, b = rgb
    min_dist = float('inf')
    best_match = "Unknown"
    
    # Check each legend entry
    for entry in legend['legend_data']:
        lr, lg, lb = entry['rgb']
        dist = math.sqrt((r - lr)**2 + (g - lg)**2 + (b - lb)**2)
        if dist < min_dist:
            min_dist = dist
            best_match = entry['climate']
            
    return best_match

def main():
    print(f"Loading data from {DATA_DIR}...")
    if not os.path.exists(MASTER_DATA_FILE):
        print(f"Error: File not found: {MASTER_DATA_FILE}")
        return

    world_data = load_json(MASTER_DATA_FILE)
    legend_data = load_json(LEGEND_DATA_FILE)
    
    print(f"Loading map from {CLIMATE_MAP_FILE}...")
    try:
        img = Image.open(CLIMATE_MAP_FILE)
        img = img.convert('RGB')
        width, height = img.size
        print(f"Map size: {width}x{height}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    updated_count = 0
    
    for continent in world_data['continents']:
        for country in continent['countries']:
            for city in country['cities']:
                coords = city.get('coords')
                if coords and len(coords) == 2:
                    lat, lng = coords
                    px, py = get_pixel_coords(lat, lng, width, height)
                    
                    # Sample color
                    rgb = img.getpixel((px, py))
                    
                    # Find climate
                    new_climate = get_closest_climate(rgb, legend_data)
                    
                    # Update
                    old_biome = city.get('biome', 'None')
                    
                    # Only calculate/update. 
                    # Note: We overwrite whatever was there to ensure consistency with the map.
                    if old_biome != new_climate:
                        # print(f"Updating {city['name']}: {old_biome} -> {new_climate}")
                        city['biome'] = new_climate
                        updated_count += 1
                        
    print(f"Updated {updated_count} cities.")
    save_json(MASTER_DATA_FILE, world_data)
    print("Saved master_world_data.json")

if __name__ == '__main__':
    main()
