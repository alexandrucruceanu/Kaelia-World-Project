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
MODEL_FAST = "gemini-2.5-flash-image" # Nano Banana (Speed/Efficiency)
MODEL_PRO = "gemini-3-pro-image-preview" # Nano Banana Pro (High Fidelity/Reasoning)

# Client initialization
client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        # Don't fail yet, just log
        sys.stderr.write(f"Client init error: {e}\n")

def sanitize_name(text):
    """ASCII-safe name sanitization."""
    return "".join(x for x in text if x.isascii() and (x.isalnum() or x in " _-")).strip().replace(" ", "_")

# --- PROMPT CONSTRUCTORS ---

def get_base_visual_data(entity):
    """Extracts visual data or provides defaults."""
    vd = entity.get('visual_data', {}).get('schema', {})
    if not vd:
         # Minimal fallback if no visual data
         return {
             "meta": {}, 
             "global_context": {"scene_description": entity.get('desc', ''), "atmosphere": "Generic"},
             "composition": {},
             "objects": []
         }
    return vd

def construct_landscape_main(entity):
    """
    Variation 1: High Aerial View (The Pattern)
    Focus: The geometry and sprawl of the city.
    Aspect Ratio: 4:3
    """
    vd = get_base_visual_data(entity)
    name = entity.get('name')
    biome = entity.get('biome', 'Unknown Biome')
    
    prompt = {
      "meta": {
        "image_type": "Ultra-High Altitude Aerial Photography, Satellite view, Photorealistic",
        "aspect_ratio": "4:3"
      },
      "global_context": {
        "scene_description": f"An immense metropolitan sprawl of {name} ({biome}) viewed from thousands of feet up. {vd.get('global_context', {}).get('scene_description', '')}",
        "lighting": "Mid-day sun casting long, distinct shadows from skyscrapers, revealing depth.",
        "atmosphere": "Overwhelming scale, detached, geometric, organized chaos."
      },
      "composition": {
        "camera_angle": "Top-down (Nadir) view, 90-degree angle looking straight at the earth.",
        "focal_point": "The complex dense grid of streets and the varied textures of rooftops."
      },
      "objects": [
        {
          "id": "city_infrastructure_main_character",
          "type": "The Urban Grid",
          "visual_attributes": {
            "architectural_style": f"A dense mix of high-rises, industrial zones, and transport arteries typical of {name}.",
            "materials_surfaces": "A tapestry of grey concrete, black asphalt, and reflective glass tops.",
            "status_activity": "Static, massive, dominating the frame from edge to edge."
          }
        },
        {
          "id": "inhabitants_and_traffic",
          "type": "Atmospheric Texture",
          "visual_attributes": {
            "density": "Heavy traffic appearing as non-distinct streams of ants.",
            "fixtures": "Highways look like veins; trains look like small threads.",
            "flow": "People are indistinguishable dots, providing scale only."
          }
        }
      ]
    }
    return json.dumps(prompt, indent=2)

def construct_landscape_seq1(entity):
    """
    Variation 2: Eye Level Street View (The Canyon)
    Focus: The vertical dominance of the buildings over the viewer.
    Aspect Ratio: 4:3
    """
    name = entity.get('name')
    
    prompt = {
      "meta": {
        "image_type": "Realistic Street Photography, 50mm lens look, Candid",
        "aspect_ratio": "4:3"
      },
      "global_context": {
        "scene_description": f"Standing on the pavement in the middle of a dense district in {name}.",
        "lighting": "Natural daylight struggling to reach the street bottom, creating strong shadows.",
        "atmosphere": "Claustrophobic, imposing, grounded, dwarfed by concrete and steel."
      },
      "composition": {
        "camera_angle": "Eye-level (approx 1.7m height), looking straight down the avenue.",
        "focal_point": "The immense verticality of the skyscraper facades receding into the distance."
      },
      "objects": [
        {
          "id": "city_architecture_main_character",
          "type": "Towering Facades",
          "visual_attributes": {
            "architectural_style": "Domineering skyscrapers made of steel, glass, and stone blocks.",
            "materials_surfaces": "Detailed textures: wet asphalt, granite curbs, metal utility poles.",
            "status_activity": "Looming over the street, blocking out most of the sky."
          }
        },
        {
          "id": "inhabitants_as_scenery",
          "type": "Pedestrian Flow",
          "visual_attributes": {
            "density": "Moderate crowd, anonymous.",
            "fixtures": "People shown with slight motion blur.",
            "flow": "A collective stream of commuters acting as scale reference only."
          }
        }
      ]
    }
    return json.dumps(prompt, indent=2)

def construct_landscape_seq2(entity):
    """
    Variation 3: Photojournalism / Realistic (The Texture)
    Focus: The grit, decay, and reality of the infrastructure.
    Aspect Ratio: 4:3
    """
    name = entity.get('name')
    
    prompt = {
      "meta": {
        "image_type": "Documentary Photojournalism, Raw Color Grade, Film Grain",
        "aspect_ratio": "4:3"
      },
      "global_context": {
        "scene_description": f"A raw, unvarnished look at a working-class district or transit hub in {name}.",
        "lighting": "Overcast, flat, diffused light highlighting grime and texture.",
        "atmosphere": "Gritty, authentic, chaotic, functional, lived-in."
      },
      "composition": {
        "camera_angle": "Wide-angle lens (e.g., 28mm) capturing a busy intersection.",
        "focal_point": "Complex layers of infrastructure: elevated train tracks over a busy street."
      },
      "objects": [
        {
          "id": "city_texture_main_character",
          "type": "Urban Infrastructure and Decay",
          "visual_attributes": {
            "architectural_style": "Functional brutalism, aging infrastructure.",
            "materials_surfaces": "Stained concrete, rusted steel bridges, peeling advertisements.",
            "status_activity": "Under constant stress, showing wear and tear."
          }
        },
        {
          "id": "inhabitants_as_ecosystem",
          "type": "The Urban Crowd",
          "visual_attributes": {
            "density": "Dense, chaotic throng.",
            "fixtures": "A jumble of umbrellas and coats merging into a single mass.",
            "flow": "People are merely part of the city's machinery."
          }
        }
      ]
    }
    return json.dumps(prompt, indent=2)

def construct_heraldry_flag(entity):
    """
    Wiki Asset JSON Template (Flags)
    Aspect Ratio: 3:2
    """
    h = entity.get('heraldry', {})
    desc = h.get('description', 'Standard flag design')
    motto = h.get('motto', '')
    
    prompt = {
      "meta": {
        "image_type": "Flat Vector Illustration, Wiki Flag",
        "aspect_ratio": "3:2"
      },
      "global_context": {
        "background_setting": "Solid White",
        "lighting": "Flat color only",
        "style_guide": "Vexillological standard, minimal detail"
      },
      "composition": {
        "view_type": "Orthographic Front View",
        "framing": "Full bleed (edge-to-edge)"
      },
      "objects": [
        {
          "id": "base_field",
          "type": "Flag Rectangle",
          "visual_attributes": {
            "division_pattern": "Geometric partition (e.g., Triband, Quarterly, Chevron, Solid)",
            "color_palette": "Standard heraldic colors",
            "border_outline": "None"
          }
        },
        {
          "id": "heraldic_charge",
          "type": "Central Emblem",
          "visual_attributes": {
            "identity": desc,
            "placement": "Centered",
            "rendering_style": "Flat graphic silhouette, Minimalist, No internal gradients"
          }
        }
      ]
    }
    return json.dumps(prompt, indent=2)

def construct_heraldry_arms(entity):
    """
    Wiki Asset JSON Template (Coat of Arms)
    Aspect Ratio: 1:1
    """
    h = entity.get('heraldry', {})
    desc = h.get('description', 'Standard shield design')
    
    prompt = {
      "meta": {
        "image_type": "Flat Vector Illustration, Wiki Coat of Arms",
        "aspect_ratio": "1:1"
      },
      "global_context": {
        "background_setting": "Transparent",
        "lighting": "Flat color only",
        "style_guide": "Heraldic coloring, bold outlines"
      },
      "composition": {
        "view_type": "Orthographic Front View",
        "framing": "Centered Heater Shield shape"
      },
      "objects": [
        {
          "id": "base_field",
          "type": "Heater Shield",
          "visual_attributes": {
            "division_pattern": "Quarterly or Solid",
            "color_palette": "Standard heraldic colors",
            "border_outline": "Thick black outline"
          }
        },
        {
          "id": "heraldic_charge",
          "type": "Primary Icon",
          "visual_attributes": {
            "identity": desc,
            "placement": "Overlaid across the center",
            "rendering_style": "Simplified vector shape"
          }
        }
      ]
    }
    return json.dumps(prompt, indent=2)

# --- GENERATION LOGIC ---

def generate_image(prompt, output_path, model, aspect_ratio="4:3"):
    path_obj = Path(output_path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    if not client:
        sys.stderr.write("No configured client.\n")
        return False

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="1K"
                )
            )
        )

        for part in response.parts:
            if part.inline_data:
                with open(path_obj, 'wb') as f:
                    f.write(part.inline_data.data)
                return True
                
    except Exception as e:
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

def export_prompts(data, filename):
    output_lines = ["# Image Generation Prompts\n", "This file is AUTO-GENERATED from `master_world_data.json` via `generate_assets_hybrid.py`.\n"]
    
    for continent in data.get('continents', []):
        output_lines.append(f"## Continent: {continent['name']}\n")
        for country in continent.get('countries', []):
            output_lines.append(f"### Country: {country['name']}\n")
            
            # Country Heraldry
            output_lines.append(f"#### Heraldry (Country)\n")
            output_lines.append("**Flag Prompt:**\n```json\n" + construct_heraldry_flag(country) + "\n```\n")
            output_lines.append("**Arms Prompt:**\n```json\n" + construct_heraldry_arms(country) + "\n```\n")
            
            for city in country.get('cities', []):
                output_lines.append(f"#### City: {city['name']}\n")
                output_lines.append("**Main Prompt (Aerial):**\n```json\n" + construct_landscape_main(city) + "\n```\n")
                output_lines.append("**Seq1 Prompt (Eye-Level):**\n```json\n" + construct_landscape_seq1(city) + "\n```\n")
                output_lines.append("**Seq2 Prompt (Photojournalism):**\n```json\n" + construct_landscape_seq2(city) + "\n```\n")
                output_lines.append("**Heraldry Flag:**\n```json\n" + construct_heraldry_flag(city) + "\n```\n")
                output_lines.append("**Heraldry Arms:**\n```json\n" + construct_heraldry_arms(city) + "\n```\n")
                output_lines.append("---\n")

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print(f"Exported prompts to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate assets for Kaelia.")
    parser.add_argument("--id", help="Specific Entity ID to generate for")
    parser.add_argument("--model", choices=["fast", "pro"], default="fast", help="Model tier to use")
    parser.add_argument("--type", choices=["landscape_main", "landscape_seq1", "landscape_seq2", "heraldry_flag", "heraldry_arms"], help="Asset type")
    parser.add_argument("--prompt", help="Custom prompt (overrides auto-construction)", default=None)
    parser.add_argument("--output", help="Explicit output file path (overrides auto-path)", default=None)
    parser.add_argument("--construct-only", action="store_true", help="Only return the constructed prompt, don't generate")
    parser.add_argument("--export-prompts", help="Export all prompts to a Markdown file", default=None)
    
    args = parser.parse_args()
    
    # Load Data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Failed to load data: {e}"}))
        return

    # Export Mode
    if args.export_prompts:
        export_prompts(data, args.export_prompts)
        return

    # Generation Mode
    if args.id:
        entity, entity_type, country_name, continent_name = get_entity_by_id(data, args.id)
        if not entity:
            print(json.dumps({"status": "error", "message": "Entity not found"}))
            return

        if args.type == "landscape_main":
            model = MODEL_PRO
        else:
            model = MODEL_FAST
        
        # Construct prompt
        # Look for stored prompt in entity data first
        stored_prompt = entity.get('prompts', {}).get(args.type)
        if stored_prompt:
            # If stored prompt is a dict, convert to json string, else use as is
            if isinstance(stored_prompt, dict):
                prompt = json.dumps(stored_prompt, indent=2)
            else:
                prompt = str(stored_prompt)
            
            # Determine aspect ratio based on type
            if "heraldry_flag" in args.type: ar = "3:2"
            elif "heraldry_arms" in args.type: ar = "1:1"
            else: ar = "4:3"
            
            # Allow manual CLI override
            if args.prompt:
                prompt = args.prompt

        # Fallback to algorithmic construction if no stored prompt
        else:
            if args.type == "landscape_main":
                prompt = args.prompt if args.prompt else construct_landscape_main(entity)
                ar = "4:3"
            elif args.type == "landscape_seq1":
                prompt = args.prompt if args.prompt else construct_landscape_seq1(entity)
                ar = "4:3"
            elif args.type == "landscape_seq2":
                prompt = args.prompt if args.prompt else construct_landscape_seq2(entity)
                ar = "4:3"
            elif args.type == "heraldry_flag":
                prompt = args.prompt if args.prompt else construct_heraldry_flag(entity)
                ar = "3:2"
            elif args.type == "heraldry_arms":
                prompt = args.prompt if args.prompt else construct_heraldry_arms(entity)
                ar = "1:1"
            else:
                prompt = "Generic Prompt"
                ar = "1:1"

        # If construct-only mode, just return the prompt
        if args.construct_only:
            print(json.dumps({
                "status": "success",
                "prompt": prompt,
                "type": args.type,
                "entity_name": entity.get('name')
            }))
            return
        
        # Determine output path if not provided
        if args.output:
            output_path = args.output
            output_rel = os.path.relpath(output_path, os.path.join(SCRIPT_DIR, "..")).replace("\\", "/")
        else:
            output_path = "output.png" 
            output_rel = "output.png"
        
        # Generate
        success = generate_image(prompt, output_path, model, ar)
        
        # Return JSON result
        result = {
            "status": "success" if success else "error",
            "image_path": output_rel,
            "prompt_used": prompt,
            "model_used": model,
            "type": args.type
        }
        print(json.dumps(result))

if __name__ == "__main__":
    main()
