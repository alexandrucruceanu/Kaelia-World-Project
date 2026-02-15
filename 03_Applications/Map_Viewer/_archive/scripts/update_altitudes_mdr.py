import struct
import json
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MDR_FILE = os.path.join(BASE_DIR, '01_Design_Sources', 'Kaelia Equirectangular.mdr')
DATA_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'master_world_data.json')

# MDR Specs
HEADER_SIZE = 1024
WIDTH = 8192
HEIGHT = 4096

def get_elevation(lat, lng, f):
    x_pct = lng / 2000.0
    y_pct = 1.0 - (lat / 1000.0)
    
    px = int(x_pct * WIDTH)
    py = int(y_pct * HEIGHT)
    
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
        
        count = 0
        for continent in world_data.get('continents', []):
            for country in continent.get('countries', []):
                for city in country.get('cities', []):
                    coords = city.get('coords', [])
                    if len(coords) == 2:
                        elev = get_elevation(coords[0], coords[1], f_mdr)
                        # We only want positive elevations for cities (clamping to 0 for sea level if negative)
                        # or keep negative if intended? Usually cities aren't under 3km of water.
                        # I'll keep the raw value but maybe round it.
                        city['altitude'] = f"{int(round(elev))}m"
                        count += 1

        with open(DATA_FILE, 'w', encoding='utf-8') as f_json:
            json.dump(world_data, f_json, indent=2)
            
        print(f"Successfully updated {count} cities using MDR data.")

if __name__ == "__main__":
    main()
