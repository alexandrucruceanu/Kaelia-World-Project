import json
import os
import sys

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")

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
    Variation 1: High Aerial View (The Pattern) -> Modified to OBLIQUE
    Focus: The geometry and sprawl of the city.
    Aspect Ratio: 4:3
    """
    vd = get_base_visual_data(entity)
    name = entity.get('name')
    biome = entity.get('biome', 'Unknown Biome')
    
    prompt = {
      "meta": {
        "image_type": "High Altitude Aerial Photography, Bird's Eye View, Photorealistic",
        "aspect_ratio": "4:3"
      },
      "global_context": {
        "scene_description": f"An immense metropolitan sprawl of {name} ({biome}) viewed from high above. {vd.get('global_context', {}).get('scene_description', '')}",
        "lighting": "Golden hour sunlight casting distinct, long shadows to reveal building heights and topography.",
        "atmosphere": "Grand, expansive, detailed, a living map."
      },
      "composition": {
        "camera_angle": "High-angle oblique view (45-degree angle), looking down across the city, NOT straight down.",
        "focal_point": "The central district rising from the surrounding sprawl, showing the 3D volume of the city."
      },
      "objects": [
        {
          "id": "city_infrastructure_main_character",
          "type": "The Urban Grid",
          "visual_attributes": {
            "architectural_style": f"A dense mix of high-rises, industrial zones, and transport arteries typical of {name}.",
            "materials_surfaces": "A tapestry of rooftops, facades, and street canyons visible from above.",
            "status_activity": "Static, massive, dominating the frame."
          }
        },
        {
          "id": "inhabitants_and_traffic",
          "type": "Atmospheric Texture",
          "visual_attributes": {
            "density": "Heavy traffic appearing as streams of light or movement.",
            "fixtures": "Highways look like ribbons; trains look like threads.",
            "flow": "City life visible as a collective flow."
          }
        }
      ]
    }
    return prompt

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
    return prompt

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
    return prompt

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
    return prompt

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
    return prompt

def migrate():
    print(f"Loading data from {DATA_FILE}...")
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    count = 0
    
    for continent in data.get('continents', []):
        for country in continent.get('countries', []):
            # Country Heraldry handled same as cities for prompts used? 
            # Currently generator only really does cities mostly but supports ID lookup.
            # Let's add prompts to countries too if they have heraldry.
            
            # Country Prompts (Heraldry)
            if 'heraldry' in country:
                current_prompts = country.get('prompts', {})
                # Generate new ones - overwrite or append
                current_prompts['heraldry_flag'] = construct_heraldry_flag(country)
                current_prompts['heraldry_arms'] = construct_heraldry_arms(country)
                country['prompts'] = current_prompts
                # print(f"Updated country: {country['name']}")

            for city in country.get('cities', []):
                # City Prompts
                prompts = {
                    "landscape_main": construct_landscape_main(city),
                    "landscape_seq1": construct_landscape_seq1(city),
                    "landscape_seq2": construct_landscape_seq2(city),
                    "heraldry_flag": construct_heraldry_flag(city),
                    "heraldry_arms": construct_heraldry_arms(city)
                }
                
                city['prompts'] = prompts
                count += 1
                # print(f"Updated city: {city['name']}")

    print(f"Migration complete. Updated {count} cities.")
    
    # Save back
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {DATA_FILE}")

if __name__ == "__main__":
    migrate()
