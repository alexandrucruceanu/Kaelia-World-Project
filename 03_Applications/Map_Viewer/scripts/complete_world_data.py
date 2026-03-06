
import os
import json
import time
import argparse
import sys
import re
from pathlib import Path
from google import genai
from google.genai import types

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")
CODEX_FILE = os.path.join(SCRIPT_DIR, "..", "..", "..", "WORLD_CODEX.md")
PROMPTS_FILE = os.path.join(SCRIPT_DIR, "..", "..", "..", "IMAGE_GENERATION_PROMPTS.md")

CONTINENT_COLORS = {
    "Nordica": ["#3498db", "#8e44ad", "#2c3e50", "#bdc3c7"],
    "Kasy Federation": ["#f39c12", "#e67e22", "#d35400", "#f1c40f"],
    "Betereko": ["#ecf0f1", "#95a5a6", "#7f8c8d"],
    "The Mirelands": ["#1abc9c", "#16a085", "#27ae60", "#2ecc71"],
    "Antarmund": ["#e74c3c", "#c0392b", "#e67e22", "#9b59b6"]
}

if not API_KEY:
    print("Error: GEMINI_API_KEY not set.")
    exit(1)

client = genai.Client(api_key=API_KEY)

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_color(continent_name, index):
    themes = CONTINENT_COLORS.get(continent_name, ["#ffffff"])
    return themes[index % len(themes)]

def clean_id(name, prefix):
    slug = re.sub(r'[^a-zA-Z0-9]', '_', name.lower()).strip('_')
    return f"{prefix}_{slug}"

def generate_lore(city_name, country_name, continent_name, context_text):
    prompt = f"""
    You are the Loremaster for Project Kaelia. 
    Generate a 2-3 sentence 'lore description' for the city '{city_name}' in {country_name}, {continent_name}.
    Context: {context_text[:15000]} 
    Task: Describe the city's unique role, atmosphere, or specific industry.
    Output JSON: {{ "desc": "The generated text..." }}
    """
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview', contents=prompt,
            config=types.GenerateContentConfig(response_mime_type='application/json')
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating lore for {city_name}: {e}")
        return None

def generate_schema(city_name, country_name, continent_name, city_desc, context_text):
    prompt = f"""
    You are the Visual Director for Project Kaelia.
    Generate a 'visual_data.schema' JSON object for the city '{city_name}' ({country_name}, {continent_name}).
    City Description: {city_desc}
    Context: {context_text[:15000]}
    
    Output JSON format:
    {{
      "meta": {{ "image_type": "Cinematic Photorealism, 8k", "aspect_ratio": "16:9" }},
      "global_context": {{ "scene_description": "...", "lighting": "...", "atmosphere": "..." }},
      "composition": {{ "camera_angle": "...", "focal_point": "..." }},
      "objects": [ {{ "id": "architecture", "visual_attributes": {{ "appearance": "..." }} }} ]
    }}
    """
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview', contents=prompt,
            config=types.GenerateContentConfig(response_mime_type='application/json')
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating schema for {city_name}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Don't save changes")
    parser.add_argument("--limit", type=int, default=100, help="Limit number of AI calls")
    args = parser.parse_args()

    data = load_json(DATA_FILE)
    codex_text = load_file(CODEX_FILE)
    prompts_text = load_file(PROMPTS_FILE)
    
    changes = 0
    ai_calls = 0

    print("--- Starting Data Completion ---")

    for continent in data.get('continents', []):
        if 'id' not in continent:
            continent['id'] = clean_id(continent['name'], 'cont')
            print(f"  [ID]     Continent: {continent['name']} -> {continent['id']}")
            changes += 1

        for country in continent.get('countries', []):
            if 'id' not in country:
                country['id'] = clean_id(country['name'], 'country')
                print(f"  [ID]     Country: {country['name']} -> {country['id']}")
                changes += 1
            
            for i, city in enumerate(country.get('cities', [])):
                ci_name = city.get('name')
                
                # Color
                if not city.get('color'):
                    new_color = get_color(continent['name'], i)
                    city['color'] = new_color
                    print(f"  [COLOR]  {ci_name}: {new_color}")
                    changes += 1

                # Lore
                if (not city.get('lore')) and ai_calls < args.limit:
                    print(f"  [LORE]   Generating for {ci_name}...")
                    lore = generate_lore(ci_name, country['name'], continent['name'], codex_text)
                    if lore:
                        city['lore'] = {"desc": lore.get('desc'), "source": "AI Generated"}
                        print(f"           -> {lore.get('desc')[:50]}...")
                        ai_calls += 1; changes += 1
                        time.sleep(1)

                # Schema
                try:
                    if (not city.get('visual_data', {}).get('schema')) and ai_calls < args.limit:
                        print(f"  [SCHEMA] Generating for {ci_name}...")
                        desc = city.get('lore', {}).get('desc', city.get('desc', ''))
                        schema = generate_schema(ci_name, country['name'], continent['name'], desc, prompts_text)
                        
                        if schema:
                            if isinstance(schema, list):
                                print(f"           [WARN] Schema returned as list, taking first item.")
                                schema = schema[0] if schema else {}
                            
                            if isinstance(schema, dict):
                                if 'visual_data' not in city: city['visual_data'] = {}
                                city['visual_data']['schema'] = schema
                                obj_count = len(schema.get('objects', []))
                                print(f"           -> Generated schema with {obj_count} objects")
                                ai_calls += 1; changes += 1
                                time.sleep(1)
                            else:
                                print(f"           [ERR] Invalid schema format: {type(schema)}")
                except Exception as e:
                    print(f"           [ERR] Failed processing {ci_name}: {e}")


    print(f"--- Finished. {changes} changes. {ai_calls} AI calls. ---")
    if not args.dry_run:
        save_json(data, DATA_FILE)
        print("Data saved.")
    else:
        print("Dry run - no save.")

if __name__ == "__main__":
    main()
