import os
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

# config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")

def create_placeholder(path, text, color, size=(800, 600)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new('RGB', size, color=color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Draw Text
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_w) / 2
    y = (size[1] - text_h) / 2
    
    d.text((x, y), text, fill=(255, 255, 255), font=font)
    img.save(path)
    print(f"Created: {os.path.basename(path)}")
    
def sanitize_name(text):
    return "".join(x for x in text if x.isascii() and (x.isalnum() or x in " _-")).strip().replace(" ", "_")

def main():
    print("WARNING: This will DELETE all existing city images and heraldry.")
    confirm = input("Type 'yes' to confirm: ")
    if confirm != "yes":
        print("Aborted.")
        return

    # 1. Load Data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Iterate and Reset
    for continent in data.get('continents', []):
        c_name = sanitize_name(continent['name'])
        
        for country in continent.get('countries', []):
            co_name = sanitize_name(country['name'])
            
            # Country Heraldry Placeholders
            flag_path = os.path.join(ASSETS_DIR, "heraldry", "flags", f"country_{co_name}.png")
            arms_path = os.path.join(ASSETS_DIR, "heraldry", "arms", f"country_{co_name}.png")
            create_placeholder(flag_path, f"Flag of {country['name']}", "#444444", size=(300, 200))
            create_placeholder(arms_path, f"Arms of {country['name']}", "#555555", size=(200, 200))

            for city in country.get('cities', []):
                ci_name = sanitize_name(city['name']).lower()
                
                # City Dir
                city_dir = os.path.join(ASSETS_DIR, "images", c_name, co_name, ci_name)
                
                # DELETE existing directory content if exists
                if os.path.exists(city_dir):
                    shutil.rmtree(city_dir)
                    print(f"Deleted {city_dir}")
                
                # PLACEHOLDERS
                create_placeholder(os.path.join(city_dir, f"{ci_name}_main.png"), f"{city['name']} (Main Aerial)", "#2c3e50")
                create_placeholder(os.path.join(city_dir, f"{ci_name}_seq1.png"), f"{city['name']} (Seq 1)", "#34495e")
                create_placeholder(os.path.join(city_dir, f"{ci_name}_seq2.png"), f"{city['name']} (Seq 2)", "#7f8c8d")
                
                # Update JSON path for main image only (legacy compatibility)
                city['image'] = f"assets/images/{c_name}/{co_name}/{ci_name}/{ci_name}_main.png"
                
                # City Heraldry
                c_flag_path = os.path.join(ASSETS_DIR, "heraldry", "flags", f"city_{ci_name}.png")
                c_arms_path = os.path.join(ASSETS_DIR, "heraldry", "arms", f"city_{ci_name}.png")
                
                # Delete old heraldry if checking existence (shutil.rmtree on parent would be too aggressive for heraldry folder)
                if os.path.exists(c_flag_path): os.remove(c_flag_path)
                if os.path.exists(c_arms_path): os.remove(c_arms_path)

                create_placeholder(c_flag_path, f"Flag of {city['name']}", "#2980b9", size=(300, 200))
                create_placeholder(c_arms_path, f"Arms of {city['name']}", "#8e44ad", size=(200, 200))
                
                # Update JSON heraldry paths
                if 'heraldry' not in city: city['heraldry'] = {}
                city['heraldry']['flag'] = f"/assets/heraldry/flags/city_{ci_name}.png"
                city['heraldry']['coat_of_arms'] = f"/assets/heraldry/arms/city_{ci_name}.png"

    # Save updated JSON links
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Updated master_world_data.json with new placeholder paths.")

if __name__ == "__main__":
    main()
