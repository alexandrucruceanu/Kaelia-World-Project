import json
import os
from PIL import Image

# ... (rest of the code is identical) ...
# I will rewrite the full code content here.

import json
import os
from PIL import Image

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'master_world_data.json')
ALTITUDE_MAP_FILE = os.path.join(BASE_DIR, 'data', 'altitude_map.jpg')
MAP_WIDTH = 6000
MAP_HEIGHT = 3000
MAX_ALTITUDE = 8848

def get_altitude_at(lat, lng, img_data, width, height):
    # Coordinate Mapping (Matches app.js)
    # Lat: 0-1000 -> Y (Leaflet 1000 is top, Canvas 0 is top)
    # Lng: 0-2000 -> X
    
    # Normalize Height (Y)
    # Leaflet Y: 0 to 1000. Canvas Y: 3000 to 0. (Actually top is 0 in canvas)
    # Wait, in app.js: yPct = 1 - (lat / 1000); pixelY = floor(yPct * mapHeight)
    # If lat 1000 (top), yPct 0 -> pixelY 0. Correct.
    y_pct = 1 - (lat / 1000.0)
    pixel_y = int(y_pct * height)
    
    # Normalize Width (X)
    # Leaflet X: 0 to 2000. Canvas X: 0 to 6000.
    x_pct = lng / 2000.0
    pixel_x = int(x_pct * width)
    
    # Bounds Check
    pixel_x = max(0, min(pixel_x, width - 1))
    pixel_y = max(0, min(pixel_y, height - 1))
    
    try:
        pixel = img_data.getpixel((pixel_x, pixel_y))
        
        val = 0
        if isinstance(pixel, int):
            val = pixel
        else:
            val = pixel[0] # R channel
            
        # Non-Blended map seems to be inverted: 255 (white) = Sea Level, 
        # Lower values = Higher land.
        # However, 0 is very dark. 
        # Let's try: Altitude = (1.0 - (val / 255.0)) * MAX_ALTITUDE
        # Ocean (white) will be 0m.
        
        meters = int(round((1.0 - (val / 255.0)) * MAX_ALTITUDE))
        return f"{meters}m"
        
    except Exception as e:
        print(f"Error sampling {pixel_x},{pixel_y}: {e}")
        return "Unknown"

def main():
    print(f"Loading Map: {ALTITUDE_MAP_FILE}")
    try:
        with Image.open(ALTITUDE_MAP_FILE) as img:
            img = img.convert("RGB")
            width, height = img.size
            if width != MAP_WIDTH or height != MAP_HEIGHT:
                print(f"Warning: Map dimensions {width}x{height} do not match expected {MAP_WIDTH}x{MAP_HEIGHT}")
            
            print(f"Loading Data: {DATA_FILE}")
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                world_data = json.load(f)
            
            count = 0
            for continent in world_data.get('continents', []):
                for country in continent.get('countries', []):
                    for city in country.get('cities', []):
                        coords = city.get('coords', [])
                        if len(coords) == 2:
                            lat = coords[0]
                            lng = coords[1]
                            new_alt = get_altitude_at(lat, lng, img, width, height)
                            city['altitude'] = new_alt
                            count += 1
                            # print(f"Updated {city.get('name', 'Unknown')}: {new_alt}")

            print(f"Saving Data... ({count} cities updated)")
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(world_data, f, indent=2)
                
            print("Done.")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
