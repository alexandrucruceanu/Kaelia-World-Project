
import json

DATA_FILE = r"c:\Proyectos_Local\Software-Development\Simulations\World_Building_Project\03_Applications\Map_Viewer\data\master_world_data.json"

def verify_move():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    found_in_oighear = False
    found_in_gryning = False

    for continent in data['continents']:
        for country in continent['countries']:
            for city in country['cities']:
                if city['name'] == "Kaldakinn":
                    print(f"Found Kaldakinn in {country['name']}")
                    if country['name'] == "Oighear":
                        found_in_oighear = True
                    elif country['name'] == "Gryning":
                        found_in_gryning = True

    if found_in_oighear and not found_in_gryning:
        print("SUCCESS: Kaldakinn is in Oighear.")
    else:
        print("FAILURE: Kaldakinn not correctly moved.")

if __name__ == "__main__":
    verify_move()
