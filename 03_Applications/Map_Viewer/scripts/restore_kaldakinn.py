
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "restore_log.txt")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def restore_kaldakinn():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        
    log("Checking for Kaldakinn...")
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 1. Check if Kaldakinn exists anywhere
        found = False
        kaldakinn_city = None
        
        for continent in data['continents']:
            for country in continent['countries']:
                for img_city in country.get('cities', []):
                    if img_city['name'] == 'Kaldakinn':
                        log(f"✅ Found Kaldakinn in {country['name']}")
                        found = True
                        kaldakinn_city = img_city
                        # If found in Gryning, move it? 
                        # User wants it in Oighear.
                        if country['name'] == 'Gryning':
                            log("⚠️  It is in Gryning. Moving to Oighear...")
                            # Remove from Gryning
                            country['cities'] = [c for c in country['cities'] if c['name'] != 'Kaldakinn']
                            # Will add to Oighear later
                            found = False 
                        break
        
        if not found:
            log("❌ Kaldakinn not found. Restoring to Oighear...")
            
            # Find Oighear
            oighear = None
            for continent in data['continents']:
                for country in continent['countries']:
                    if country['name'] == 'Oighear':
                        oighear = country
                        break
            
            if oighear:
                # Create Kaldakinn
                new_city = {
                    "id": "city_kaldakinn_restored",
                    "name": "Kaldakinn",
                    "type": "village",
                    "coords": [880, 260],
                    "biome": "Alpine Tundra",
                    "population": "450",
                    "desc": "Glacier research hamlet.",
                    "color": "#eeeeee",
                    "visual_data": {}, 
                    "altitude": 1400,
                    "heraldry": {},
                    "lore": { "desc": "A small research outpost dedicated to monitoring the glacial movements." },
                    "prompts": {},
                    "countryName": "Oighear",
                    "continentName": "Nordica"
                }
                
                if 'cities' not in oighear: oighear['cities'] = []
                oighear['cities'].append(new_city)
                log("✅ Added Kaldakinn to Oighear.")
                
                # Save
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                log("✅ Saved master_world_data.json.")
                
            else:
                log("❌ Oighear not found!")
                
    except Exception as e:
        log(f"❌ Error: {e}")

if __name__ == "__main__":
    restore_kaldakinn()
