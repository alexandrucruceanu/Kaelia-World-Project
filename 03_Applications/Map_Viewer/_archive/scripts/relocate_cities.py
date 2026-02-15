import struct
import json
import os
import numpy as np

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MDR_FILE = os.path.join(BASE_DIR, '01_Design_Sources', 'Kaelia Equirectangular.mdr')
DATA_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'master_world_data.json')

# MDR Specs
HEADER_SIZE = 1024
WIDTH = 8192
HEIGHT = 4096

def get_elevation_at_pixel(px, py, elevations):
    return elevations[py, px]

def find_nearest_land(start_px, start_py, elevations):
    """Spiral search for nearest pixel with elevation > 0."""
    max_search_dist = 500 # Max radius to search (in pixels)
    
    for dist in range(1, max_search_dist):
        # Top and bottom edges
        for dx in range(-dist, dist + 1):
            for dy in [-dist, dist]:
                px, py = start_px + dx, start_py + dy
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    if elevations[py, px] > 0:
                        return px, py
        
        # Left and right edges (excluding corners already checked)
        for dy in range(-dist + 1, dist):
            for dx in [-dist, dist]:
                px, py = start_px + dx, start_py + dy
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    if elevations[py, px] > 0:
                        return px, py
                        
    return None, None

def main():
    if not os.path.exists(MDR_FILE):
        print(f"MDR File not found: {MDR_FILE}")
        return

    print(f"Loading terrain data from {MDR_FILE}...")
    with open(MDR_FILE, 'rb') as f_mdr:
        f_mdr.seek(HEADER_SIZE)
        raw_data = f_mdr.read()
        elevations = np.frombuffer(raw_data, dtype='<f4').reshape((HEIGHT, WIDTH))

    with open(DATA_FILE, 'r', encoding='utf-8') as f_json:
        world_data = json.load(f_json)

    moved_count = 0
    total_cities = 0
    
    print("\nChecking city positions...")
    for continent in world_data.get('continents', []):
        for country in continent.get('countries', []):
            for city in country.get('cities', []):
                total_cities += 1
                name = city.get('name', 'Unknown')
                coords = city.get('coords', [])
                if len(coords) != 2: continue
                
                lat, lng = coords
                x_pct = lng / 2000.0
                y_pct = 1.0 - (lat / 1000.0)
                px = int(round(x_pct * WIDTH))
                py = int(round(y_pct * HEIGHT))
                
                # Clamp to avoid index errors
                px = max(0, min(px, WIDTH - 1))
                py = max(0, min(py, HEIGHT - 1))
                
                elev = elevations[py, px]
                
                if elev <= 0:
                    print(f"City '{name}' is in ocean (Elev: {elev:.2f}m) at ({lat}, {lng}). Searching for land...")
                    new_px, new_py = find_nearest_land(px, py, elevations)
                    
                    if new_px is not None:
                        new_lat = round(1000.0 * (1.0 - (new_py / HEIGHT)), 2)
                        new_lng = round(2000.0 * (new_px / WIDTH), 2)
                        new_elev = elevations[new_py, new_px]
                        
                        dist_px = np.sqrt((new_px - px)**2 + (new_py - py)**2)
                        
                        print(f"  -> Moved to ({new_lat}, {new_lng}). New Elev: {new_elev:.2f}m. Dist: {dist_px:.1f}px")
                        
                        city['coords'] = [new_lat, new_lng]
                        city['altitude'] = f"{int(round(new_elev))}m"
                        moved_count += 1
                    else:
                        print(f"  !! WARNING: Could not find land nearby for '{name}'")
                else:
                    # Just update altitude string to match precise MDR if needed
                    city['altitude'] = f"{int(round(elev))}m"

    if moved_count > 0:
        with open(DATA_FILE, 'w', encoding='utf-8') as f_json:
            json.dump(world_data, f_json, indent=2)
        print(f"\nSuccessfully moved {moved_count} cities to land. Updated {DATA_FILE}")
    else:
        print("\nAll cities are already on land.")

if __name__ == "__main__":
    main()
