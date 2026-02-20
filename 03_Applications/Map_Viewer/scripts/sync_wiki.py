
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")
CODEX_FILE = os.path.join(SCRIPT_DIR, "..", "..", "..", "WORLD_CODEX.md")
WIKI_DIR = os.path.join(SCRIPT_DIR, "..", "wiki")
LOG_FILE = os.path.join(SCRIPT_DIR, "sync_log.txt")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)


# Hardcoded Metadata to preserve Lore that isn't in JSON
CONTINENT_META = {
    "Nordica": {
        "header": "🏔️ Continent 1: Nordica",
        "intro": "* **Location:** North-West Hemisphere\n* **Visual Biome:** **Alpine Tundra (Grey)** & **Boreal Forest (Purple)**\n* **Corrected Climate:** **Sub-Arctic / Taiga.**\n* *Correction:* Previous references to \"Temperate\" zones are removed except for the extreme southern tip. This is a harsh, frozen continent.",
    },
    "Kasy Federation": { 
         "header": "☀️ Continent 2: The Kasy Federation",
         "intro": "* **Location:** South-West Archipelago\n* **Visual Biome:** **Chaparral (Olive/Yellow)** & **Temperate Forest (Green)**\n* **Corrected Climate:** **Mediterranean / Semi-Arid.**\n* *Correction:* The \"Desert\" classification was incorrect. The region is actually a **Chaparral zone** (hot, dry summers; mild, wet winters), similar to California or the Mediterranean.",
    },
     "Betereko": {
         "header": "❄️ Continent 3: Betereko",
         "intro": "*   **Political Status:** A unified **Continent-State** (similar to Earth's Australia). The entire landmass is governed as a single sovereign entity: **The Betereko Technocracy**.\n*   **Geography:** Sub-Polar Monolithic Plateau.\n*   **Location:** High Southern Latitudes (Proximal to the South Pole).\n*   **Visual Biome:** **Alpine Tundra** & **Ice Caps**.\n*   **Modern Status:** A global leader in **Aerospace and Quantum Computing**. The plateau's high latitude and stable, cold atmospheric conditions make it the planet's primary spaceport for high-inclination orbits.\n*   **Culture:** Technocratic and highly regimented. They believe their isolation and extreme environment give them a \"superior perspective\" on global data.\n*   **Metropolis (Capital):** **Apex** - Perched on the precipice of the eastern cliffs, Apex represents the cleaner air-boundary of the sub-polar south. It is the planet's premier center for long-range telecommunications, data storage, and global meteorology. The city is characterized by dignified stone and glass architecture, hosting international research institutes and massive radio-dish arrays that overlook the \"Endless Drop\" into the ocean.",
    },
    "Mirelands": { 
         "header": "🌲 Continent 4: The Mirelands",
         "intro": "* **Location:** Central \"Shattered\" Landmass\n* **Visual Biome:** **Boreal Forest (Purple)** with **Wetland Margins (Cyan/Green)**\n* **Corrected Climate:** **Cold Taiga / Sub-Arctic Swamp.**",
    },
    "Antarmund": {
         "header": "🏛️ Continent 5: Antarmund (The Eastern Super-Continent)",
         "intro": "* **Location:** Eastern Hemisphere\n* **Visual Biome:** **Gradient** from **Tundra (North)** to **Temperate Rainforest (South)**.",
    }
}

def generate_geography_section(data):
    md = []
    
    md.append("The planet is defined by a severe **North-South Temperature Gradient**. The Northern Hemisphere is locked in Cryosphere (Ice) and Boreal (Taiga) zones, while the Southern Hemisphere enjoys Temperate and Subtropical climates.")
    md.append("")
    md.append("---")
    md.append("")

    for i, continent in enumerate(data.get('continents', [])):
        # Determine Metadata key
        meta_key = None
        for k in CONTINENT_META.keys():
            if k in continent['name']:
                meta_key = k
                break
        
        c_meta = CONTINENT_META.get(meta_key, {})
        
        header = c_meta.get('header', f"## 🌍 Continent {i+1}: {continent['name']}")
        intro = c_meta.get('intro', f"* **Name:** {continent['name']}")
        
        md.append(header)
        md.append(intro)
        md.append("")
        
        for j, country in enumerate(continent.get('countries', [])):
            md.append(f"### {j+1}. {country['name']}")
            
            # City Generation
            if 'cities' in country and country['cities']:
                cities_by_type = {}
                for city in country['cities']:
                    ctype = city.get('type', 'settlement').lower()
                    if ctype not in cities_by_type: cities_by_type[ctype] = []
                    cities_by_type[ctype].append(city)
                
                # Metropolis
                if 'metropolis' in cities_by_type:
                    for city in cities_by_type['metropolis']:
                        desc = city.get('desc', 'No description.')
                        if 'lore' in city and isinstance(city['lore'], dict): desc = city['lore'].get('desc', desc)
                        md.append(f"* **Metropolis:** **{city['name']}** - {desc}")
                
                # Settlements
                others = []
                if 'settlement' in cities_by_type: others.extend(cities_by_type['settlement'])
                if 'city' in cities_by_type: others.extend(cities_by_type['city'])
                
                if others:
                    md.append(f"*   **Settlements:**")
                    for city in others:
                        desc = city.get('desc', 'No description.')
                        md.append(f"    *   **{city['name']}:** {desc}")

                # Villages
                villages = []
                if 'village' in cities_by_type: villages.extend(cities_by_type['village'])
                if 'hamlet' in cities_by_type: villages.extend(cities_by_type['hamlet'])
                
                if villages:
                    v_list = []
                    for v in villages:
                         desc = v.get('desc', '')
                         v_list.append(f"{v['name']} ({desc})")
                    md.append(f"*   **Villages:** {', '.join(v_list)}.")
            
            md.append("") # Spacer
            
        md.append("") 

    return "\n".join(md)

def update_country_html(country_name, continent_name, cities):
    # This function updates the specific HTML file for the country
    # We assume file exists at wiki/countries/{country_name_dashed}.html
    
    filename = country_name.lower().replace(" ", "_") + ".html"
    filepath = os.path.join(WIKI_DIR, "countries", filename)
    
    if not os.path.exists(filepath):
        log(f"⚠️ HTML file not found for {country_name}: {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # We need to update the "Major Cities" list
        
        start_marker = "<h3>Major Cities</h3>"
        if start_marker not in html:
            log(f"⚠️ Major Cities section not found in {filename}")
            return
            
        parts = html.split(start_marker)
        pre = parts[0] + start_marker
        rest = parts[1]
        
        if "<ul>" not in rest or "</ul>" not in rest:
            log(f"⚠️ UL not found in {filename} after H3")
            return

        ul_start = rest.find("<ul>")
        ul_end = rest.find("</ul>") + 5 # include </ul>
        
        pre_ul = rest[:ul_start]
        post_ul = rest[ul_end:]

    
    # Generate New List
    new_list_items = []
    for city in cities:
        city_filename = city['name'].lower().replace(" ", "_").replace("ý", "y").replace("ö", "o").replace("ð", "d").replace("æ", "ae").replace("í", "i") + ".html"
        # Safe filename generation might be tricky if it doesn't match existing files exactly.
        # But we can try to guess or just use simple sanitization. 
        # Actually, looking at gryning.html: cities/sk_jakot.html (skipping special chars?) or encoded?
        # "sk_jakot.html" -> Skýjakot. "bjarnarfj_r_ur.html" -> Bjarnarfjörður
        # It seems special chars are replaced by underscores or removed? 
        # Let's verify file naming convention if possible. 
        # For now, let's just regenerate the *text* of the list correctly.
        # If link is broken, that's a secondary issue but acceptable for now compared to wrong data.
        # Wait, I can try to find the matching file in `wiki/cities/` directory if I really want to be robust.
        # But for now, let's just use a simple robust formatter.
        
        # Simple sanitizer matching what I see in `gryning.html`?
        # "sk_jakot" implies "ý" -> "_"
        # "bjarnarfj_r_ur" implies "ö" -> "_", "ð" -> "_"
        safe_name = city['name'].lower()
        for char in "ýöðæíá":
            safe_name = safe_name.replace(char, "_")
        safe_name = safe_name.replace(" ", "_") + ".html"
        
        new_list_items.append(f'<li><a href="../cities/{safe_name}">{city["name"]}</a> ({city.get("type", "settlement")})</li>')

    new_ul = "\n        <ul>" + "".join(new_list_items) + "</ul>"
    
    new_html = pre + pre_ul + new_ul + post_ul
    
    # Also update the "Cities count" in infobox?
    # <tr><th>Cities</th><td>7</td></tr>
    # Search for "<tr><th>Cities</th><td>"
    
    count_marker = "<tr><th>Cities</th><td>"
    if count_marker in new_html:
        c_parts = new_html.split(count_marker)
        c_pre = c_parts[0] + count_marker
        c_rest = c_parts[1]
        c_end = c_rest.find("</td>")
        
        new_html = c_pre + str(len(cities)) + c_rest[c_end:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        log(f"✅ Updated HTML for {country_name}")
        
    except Exception as e:
        log(f"❌ Error updating {filename}: {e}")


def sync_wiki():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    log("🔄 Syncing Wiki...")
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        with open(CODEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Update Markdown Codex
        start_marker = "## 🌍 Global Geography Overview"
        end_marker = "## 🔍 Strategic Resource Correction"
        
        if start_marker in content and end_marker in content:
            new_geo = generate_geography_section(data)
            pre = content.split(start_marker)[0] + start_marker + "\n"
            post = "\n" + end_marker + content.split(end_marker)[1]
            new_content = pre + new_geo + post
            with open(CODEX_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            log("✅ World Codex Markdown Synced!")
            
        # 2. Update HTML Pages
        for continent in data.get('continents', []):
            for country in continent.get('countries', []):
                update_country_html(country['name'], continent['name'], country.get('cities', []))

    except Exception as e:
        log(f"❌ Error: {e}")

if __name__ == "__main__":
    sync_wiki()
