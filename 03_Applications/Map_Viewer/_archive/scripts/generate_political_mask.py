from PIL import Image
import os
import json
import random
import sys

def generate_political_mask():
    # Paths
    base_path = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project"
    layers_path = os.path.join(base_path, r"02_Visual_Assets\1.0_Planet_Scale\Cartography\Exported_Layers")
    output_img_path = os.path.join(base_path, r"03_Applications\Map_Viewer\data\political_mask.png")
    output_json_path = os.path.join(base_path, r"03_Applications\Map_Viewer\data\political_lookup.json")
    master_data_path = os.path.join(base_path, r"03_Applications\Map_Viewer\data\master_world_data.json")

    print("Loading master data...", flush=True)
    # Load Continent Data
    with open(master_data_path, 'r', encoding='utf-8') as f:
        world_data = json.load(f)

    # Build Country -> Continent Map
    country_to_continent = {}
    for continent in world_data['continents']:
        for country in continent['countries']:
            country_to_continent[country['name']] = continent['name']

    # Files to exclude
    exclude = ["Background.png", "Planeta 1 Equirectangular Sphere Map B&W.png", "Planeta 1 Equirectangular Sphere Map Altitude.png", "Copia de Betereko.png"]
    
    files = [f for f in os.listdir(layers_path) if f.endswith(".png") and f not in exclude]
    files.sort() # Deterministic order
    
    if not files:
        print("No files found.", flush=True)
        return

    # Base Canvas
    first_img = Image.open(os.path.join(layers_path, files[0]))
    width, height = first_img.size
    print(f"Creating mask {width}x{height}...", flush=True)
    mask = Image.new("RGB", (width, height), (0, 0, 0)) # Default Black = Ocean/Unknown
    lookup = {}

    used_colors = set()
    used_colors.add("0,0,0")

    processed_count = 0

    # Deterministic Random Seed for consistent colors
    random.seed(42)

    for filename in files:
        country_name = os.path.splitext(filename)[0]
        
        # Generate Unique Color
        while True:
            r = random.randint(10, 255)
            g = random.randint(10, 255)
            b = random.randint(10, 255)
            color_key = f"{r},{g},{b}"
            if color_key not in used_colors:
                used_colors.add(color_key)
                break
        
        print(f"Processing: {country_name} -> {color_key}", flush=True)
        
        # Determine Continent
        continent_name = country_to_continent.get(country_name, "Unknown")
        
        # Add to Lookup
        lookup[color_key] = {
            "country": country_name,
            "continent": continent_name
        }

        # Composite onto Mask
        img_path = os.path.join(layers_path, filename)
        layer = Image.open(img_path).convert("RGBA")
        
        # Create a solid color image
        solid_color = Image.new("RGBA", (width, height), (r, g, b, 255))
        
        # Paste using the layer itself as the mask (alpha channel)
        mask.paste(solid_color, (0,0), layer)
        processed_count += 1

    # Save
    print(f"Saving mask to {output_img_path}", flush=True)
    mask.save(output_img_path, "PNG")
    
    print(f"Saving lookup to {output_json_path}", flush=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(lookup, f, indent=2)

    print(f"Done! Processed {processed_count} countries.", flush=True)

if __name__ == "__main__":
    generate_political_mask()
