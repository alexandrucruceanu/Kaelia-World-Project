import os
import json
import time
import argparse
import sys
from pathlib import Path
from google import genai
from google.genai import types

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
# Use absolute path or relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")

# Models
MODEL_FAST = "gemini-2.5-flash-image" # Nano Banana (Flags/Arms) / Fast Prototyping
MODEL_PRO = "gemini-3-pro-image-preview" # Nano Banana Pro (Landscapes)

if not API_KEY:
    # Print error as JSON for the UI to catch
    print(json.dumps({"status": "error", "message": "GEMINI_API_KEY environment variable not set."}))
    exit(1)

client = genai.Client(api_key=API_KEY)

def construct_prompt_from_schema(entity):
    visual_data = entity.get('visual_data', {})
    schema = visual_data.get('schema', {})
    
    if not schema:
        # Fallback to description
        return f"{entity.get('name')}: {entity.get('desc')}"

    meta = schema.get('meta', {})
    context = schema.get('global_context', {})
    composition = schema.get('composition', {})
    
    # Construct a robust prompt
    prompt_parts = []
    
    # Subject & Type
    prompt_parts.append(f"{meta.get('image_type', 'Cinematic shot')} of {entity.get('name')}.")
    
    # Context
    if 'scene_description' in context:
        prompt_parts.append(context['scene_description'])
    if 'atmosphere' in context:
        prompt_parts.append(f"Atmosphere: {context['atmosphere']}.")
    if 'lighting' in context:
        prompt_parts.append(f"Lighting: {context['lighting']}.")
        
    # Composition
    if 'camera_angle' in composition:
        prompt_parts.append(f"Angle: {composition['camera_angle']}.")
    if 'focal_point' in composition:
        prompt_parts.append(f"Focus on {composition['focal_point']}.")
        
    # Objects/Details
    objects = schema.get('objects', [])
    obj_descs = []
    for obj in objects:
        attrs = obj.get('visual_attributes', {})
        desc = ", ".join([f"{k}: {v}" for k, v in attrs.items()])
        obj_descs.append(f"{obj.get('id')}: {desc}")
    
    if obj_descs:
        prompt_parts.append("Details: " + " | ".join(obj_descs))

    return " ".join(prompt_parts)

def generate_image(prompt, output_path, model, aspect_ratio="1:1"):
    path = Path(output_path)
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="1K" # Default to 1K for speed/cost
                )
            )
        )

        for part in response.parts:
            if part.inline_data:
                # Basic write for current SDK usage
                with open(path, 'wb') as f:
                    f.write(part.inline_data.data)
                return True
                
    except Exception as e:
        # Output error to stderr so it doesn't break JSON on stdout
        sys.stderr.write(f"Generation Error: {e}\n")
        return False
        
    return False

def get_entity_by_id(data, target_id):
    for continent in data.get('continents', []):
        for country in continent.get('countries', []):
             if country.get('id') == target_id: return country, "country", country.get('name')
             for city in country.get('cities', []):
                 if city.get('id') == target_id: return city, "city", country.get('name')
    return None, None, None

def main():
    parser = argparse.ArgumentParser(description="Generate assets for Kaelia.")
    parser.add_argument("--id", help="Specific Entity ID to generate for")
    parser.add_argument("--model", choices=["fast", "pro"], default="fast", help="Model tier to use")
    parser.add_argument("--type", choices=["landscape", "flag", "arms"], default="landscape", help="Asset type")
    
    args = parser.parse_args()
    
    # Load Data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mode: Single Entity (API Usage)
    if args.id:
        entity, entity_type, country_name = get_entity_by_id(data, args.id)
        if not entity:
            print(json.dumps({"status": "error", "message": "Entity not found"}))
            return

        model = MODEL_PRO if args.model == "pro" else MODEL_FAST
        # Landscape only valid for cities usually, but let's be flexible
        
        output_path = ""
        prompt = ""
        
        if args.type == "landscape":
            # Sanitize names
            # Use lower() for city to match legacy sequence and migration
            safe_country = "".join(x for x in country_name if x.isalnum() or x in " _-").strip().replace(" ", "_")
            safe_city = "".join(x for x in entity['name'] if x.isalnum() or x in " _-").strip().replace(" ", "_").lower()
            
            # Find Continent for structure (perf hit but cleaner)
            continent_name = "Unknown"
            for cont in data['continents']:
                for c in cont['countries']:
                    if c['name'] == country_name:
                        continent_name = cont['name']
                        break
            safe_continent = "".join(x for x in continent_name if x.isalnum() or x in " _-").strip().replace(" ", "_")

            # Structure: assets/images/{Continent}/{Country}/{City}/
            # Filename: {city_slug}_main.png or {city_slug}_{n}.png
            
            output_abs_dir = os.path.join(ASSETS_DIR, "images", safe_continent, safe_country, safe_city)
            output_rel_dir = os.path.join("assets", "images", safe_continent, safe_country, safe_city)
            os.makedirs(output_abs_dir, exist_ok=True)
            
            # Determine filename
            main_file = os.path.join(output_abs_dir, f"{safe_city}_main.png")
            if not os.path.exists(main_file):
                filename = f"{safe_city}_main.png"
            else:
                # Find next sequence
                idx = 1
                while True:
                    next_file = os.path.join(output_abs_dir, f"{safe_city}_{idx}.png")
                    if not os.path.exists(next_file):
                        filename = f"{safe_city}_{idx}.png"
                        break
                    idx += 1
            
            output_path = os.path.join(output_abs_dir, filename)
            
            prompt = construct_prompt_from_schema(entity)
            
            # Generate
            success = generate_image(prompt, output_path, model, "16:9")
            
            # Return JSON result
            result = {
                "status": "success" if success else "error",
                "image_path": os.path.join(output_rel_dir, filename).replace("\\", "/"), # Return relative path for frontend
                "prompt_used": prompt,
                "model_used": model
            }
            print(json.dumps(result))

        elif args.type in ["flag", "arms"]:
            # Logic for heraldry not requested in this UI flow yet, effectively
            print(json.dumps({"status": "error", "message": "Heraldry generation not yet hooked up to CLI"}))

    else:
        # Mode: Bulk (Legacy/Maintenance)
        print("Bulk mode not implemented in this refactor. Use --id.")

if __name__ == "__main__":
    main()
