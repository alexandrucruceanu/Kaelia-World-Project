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

def construct_heraldry_prompt(entity, heraldry_type):
    """Construct a prompt specifically for flag or coat of arms generation."""
    heraldry = entity.get('heraldry', {})
    name = entity.get('name', 'Unknown')
    desc = heraldry.get('description', '')
    motto = heraldry.get('motto', '')
    biome = entity.get('biome', '')
    
    if heraldry_type == "flag":
        prompt = f"A flat, clean national flag design for '{name}'. "
        if desc:
            prompt += f"The heraldic description is: {desc}. "
        if motto:
            prompt += f"Motto: \"{motto}\". "
        prompt += "Design should be a simple, bold flag with clean geometric shapes and vibrant colors. "
        prompt += "No text on the flag. Flat design, no 3D effects, no wrinkles, no fabric texture. "
        prompt += f"The flag should evoke the spirit of a {biome} region."
    else:  # arms
        prompt = f"A detailed coat of arms / heraldic shield for '{name}'. "
        if desc:
            prompt += f"The heraldic description is: {desc}. "
        if motto:
            prompt += f"Motto: \"{motto}\". "
        prompt += "Medieval European heraldic style with a central shield, supporters, and decorative elements. "
        prompt += "Rich, detailed illustration on a transparent or solid background. "
        prompt += f"The coat of arms should reflect a {biome} region."
    
    return prompt

def generate_image(prompt, output_path, model, aspect_ratio="1:1"):
    path_obj = Path(output_path)
    
    # Ensure directory exists
    path_obj.parent.mkdir(parents=True, exist_ok=True)

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
                with open(path_obj, 'wb') as f:
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
             if country.get('id') == target_id: return country, "country", country.get('name'), continent.get('name')
             for city in country.get('cities', []):
                 if city.get('id') == target_id: return city, "city", country.get('name'), continent.get('name')
    return None, None, None, None

def sanitize_name(text):
    """ASCII-safe name sanitization."""
    return "".join(x for x in text if x.isascii() and (x.isalnum() or x in " _-")).strip().replace(" ", "_")

def main():
    parser = argparse.ArgumentParser(description="Generate assets for Kaelia.")
    parser.add_argument("--id", help="Specific Entity ID to generate for")
    parser.add_argument("--model", choices=["fast", "pro"], default="fast", help="Model tier to use")
    parser.add_argument("--type", choices=["landscape", "flag", "arms"], default="landscape", help="Asset type")
    parser.add_argument("--prompt", help="Custom prompt (overrides auto-construction)", default=None)
    parser.add_argument("--output", help="Explicit output file path (overrides auto-path)", default=None)
    parser.add_argument("--construct-only", action="store_true", help="Only return the constructed prompt, don't generate")
    
    args = parser.parse_args()
    
    # Load Data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mode: Single Entity (API Usage)
    if args.id:
        entity, entity_type, country_name, continent_name = get_entity_by_id(data, args.id)
        if not entity:
            print(json.dumps({"status": "error", "message": "Entity not found"}))
            return

        model = MODEL_PRO if args.model == "pro" else MODEL_FAST
        
        # Construct prompt based on type
        if args.type == "landscape":
            prompt = args.prompt if args.prompt else construct_prompt_from_schema(entity)
        else:
            prompt = args.prompt if args.prompt else construct_heraldry_prompt(entity, args.type)
        
        # If construct-only mode, just return the prompt
        if args.construct_only:
            print(json.dumps({
                "status": "success",
                "prompt": prompt,
                "type": args.type,
                "entity_name": entity.get('name')
            }))
            return
        
        # Determine output path
        if args.output:
            output_path = args.output
            output_rel = os.path.relpath(output_path, os.path.join(SCRIPT_DIR, "..")).replace("\\", "/")
        elif args.type == "landscape":
            safe_continent = sanitize_name(continent_name)
            safe_country = sanitize_name(country_name)
            safe_city = sanitize_name(entity['name']).lower()
            
            output_abs_dir = os.path.join(ASSETS_DIR, "images", safe_continent, safe_country, safe_city)
            output_rel_dir = os.path.join("assets", "images", safe_continent, safe_country, safe_city)
            os.makedirs(output_abs_dir, exist_ok=True)
            
            # Always create as main or next sequence
            main_file = os.path.join(output_abs_dir, f"{safe_city}_main.png")
            if not os.path.exists(main_file):
                filename = f"{safe_city}_main.png"
            else:
                idx = 1
                while True:
                    next_file = os.path.join(output_abs_dir, f"{safe_city}_{idx}.png")
                    if not os.path.exists(next_file):
                        filename = f"{safe_city}_{idx}.png"
                        break
                    idx += 1
            
            output_path = os.path.join(output_abs_dir, filename)
            output_rel = os.path.join(output_rel_dir, filename).replace("\\", "/")
        else:
            # Heraldry: flag or arms
            safe_city = sanitize_name(entity['name']).lower()
            sub = "flags" if args.type == "flag" else "arms"
            filename = f"city_{safe_city}.png"
            output_path = os.path.join(ASSETS_DIR, "heraldry", sub, filename)
            output_rel = f"assets/heraldry/{sub}/{filename}"
        
        # Determine aspect ratio
        aspect_ratio = "16:9" if args.type == "landscape" else "1:1"
        
        # Generate
        success = generate_image(prompt, output_path, model, aspect_ratio)
        
        # Return JSON result
        result = {
            "status": "success" if success else "error",
            "image_path": output_rel,
            "prompt_used": prompt,
            "model_used": model,
            "type": args.type
        }
        print(json.dumps(result))

    else:
        # Mode: Bulk (Legacy/Maintenance)
        print("Bulk mode not implemented in this refactor. Use --id.")

if __name__ == "__main__":
    main()
