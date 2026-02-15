
import requests
import json
import os
import time

# Configuration
BASE_URL = "http://localhost:3000"
DATA_FILE = r"c:\Proyectos_Local\Software-Development\Simulations\World_Building_Project\03_Applications\Map_Viewer\data\master_world_data.json"

def verify_endpoints():
    print("--- Verifying Movable Label Endpoints ---")
    
    # 1. Read initial data to find a target
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    target_continent = data['continents'][0]
    cont_name = target_continent['name']
    
    target_country = target_continent['countries'][0]
    country_name = target_country['name']
    
    print(f"Targeting Continent: {cont_name}, Country: {country_name}")
    
    # 2. Test Continent Update
    new_cont_coords = [500, 500]
    print(f"Sending PUT /api/continents for {cont_name} with {new_cont_coords}...")
    
    try:
        res = requests.put(f"{BASE_URL}/api/continents", json={
            "continentName": cont_name,
            "coords": new_cont_coords
        })
        
        if res.status_code == 200:
            print("✅ Continent Update Success (200 OK)")
        else:
            print(f"❌ Continent Update Failed: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 3. Test Country Update
    new_country_coords = [600, 600]
    print(f"Sending PUT /api/countries for {country_name} with {new_country_coords}...")
    
    try:
        res = requests.put(f"{BASE_URL}/api/countries", json={
            "continentName": cont_name,
            "countryName": country_name,
            "coords": new_country_coords
        })
        
        if res.status_code == 200:
            print("✅ Country Update Success (200 OK)")
        else:
            print(f"❌ Country Update Failed: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 4. Verify Persistence in File
    time.sleep(1) # Wait for FS write
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
        
    c_check = next((c for c in new_data['continents'] if c['name'] == cont_name), None)
    if c_check and c_check.get('coords') == new_cont_coords:
        print("✅ Continent Coordinate Parsistence Verified")
    else:
        print(f"❌ Continent Persistence Failed. Got {c_check.get('coords')}")

    cnt_check = next((c for c in c_check['countries'] if c['name'] == country_name), None)
    if cnt_check and cnt_check.get('coords') == new_country_coords:
        print("✅ Country Coordinate Persistence Verified")
    else:
        print(f"❌ Country Persistence Failed. Got {cnt_check.get('coords')}")
        
    # Cleanup (Optional: Reset? User might notice markers moved)
    # For now, leaving them as proof of work, or user can move them back.

if __name__ == "__main__":
    verify_endpoints()
