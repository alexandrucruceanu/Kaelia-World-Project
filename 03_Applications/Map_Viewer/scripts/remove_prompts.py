import json
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
MASTER_DATA_FILE = os.path.join(DATA_DIR, 'master_world_data.json')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    print(f"Loading data from {MASTER_DATA_FILE}...")
    if not os.path.exists(MASTER_DATA_FILE):
        print(f"Error: File not found: {MASTER_DATA_FILE}")
        return

    data = load_json(MASTER_DATA_FILE)
    count = 0

    for continent in data.get('continents', []):
        for country in continent.get('countries', []):
            for city in country.get('cities', []):
                if 'visual_data' in city:
                    if 'prompt' in city['visual_data']:
                        del city['visual_data']['prompt']
                        count += 1
    
    print(f"Removed 'prompt' from {count} cities.")
    save_json(MASTER_DATA_FILE, data)
    print("Saved master_world_data.json")

if __name__ == "__main__":
    main()
