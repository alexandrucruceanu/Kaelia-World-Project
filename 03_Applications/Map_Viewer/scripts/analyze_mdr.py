import struct
import json
import os

# Paths
# __file__ is Map_Viewer/scripts/analyze_mdr.py
# 1st dirname: Map_Viewer/scripts
# 2nd: Map_Viewer
# 3rd: 03_Applications
# 4th: World_Building_Project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MDR_FILE = os.path.join(BASE_DIR, '01_Design_Sources', 'Kaelia Equirectangular.mdr')
DATA_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'master_world_data.json')

# MDR Specs
HEADER_SIZE = 1024
WIDTH = 8192
HEIGHT = 4096

def get_elevation(lat, lng, f):
    # Normalized coords (0-1)
    # Lng 0..2000 -> X 0..1
    # Lat 0..1000 -> Y 0..1 (1 is top)
    
    x_pct = lng / 2000.0
    y_pct = 1.0 - (lat / 1000.0) # Invert for top-down image coords
    
    px = int(x_pct * WIDTH)
    py = int(y_pct * HEIGHT)
    
    # Clamp
    px = max(0, min(px, WIDTH - 1))
    py = max(0, min(py, HEIGHT - 1))
    
    offset = HEADER_SIZE + (py * WIDTH + px) * 4
    f.seek(offset)
    data = f.read(4)
    if not data: return 0.0
    return struct.unpack('<f', data)[0]

def main():
    if not os.path.exists(MDR_FILE):
        print(f"MDR File not found: {MDR_FILE}")
        return

    with open(MDR_FILE, 'rb') as f_mdr:
        with open(DATA_FILE, 'r', encoding='utf-8') as f_json:
            world_data = json.load(f_json)
        
        print(f"{'City Name':<25} | {'Lat':<7} | {'Lng':<7} | {'Elevation (m)':<15}")
        print("-" * 65)
        
        for continent in world_data.get('continents', []):
            for country in continent.get('countries', []):
                for city in country.get('cities', []):
                    name = city.get('name', 'Unknown')
                    coords = city.get('coords', [])
                    if len(coords) == 2:
                        elev = get_elevation(coords[0], coords[1], f_mdr)
                        print(f"{name:<25} | {coords[0]:<7} | {coords[1]:<7} | {elev:>10.2f}m")

if __name__ == "__main__":
    main()
