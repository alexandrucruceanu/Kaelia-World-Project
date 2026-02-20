
import json
import os

DATA_FILE = r"c:\Proyectos_Local\Software-Development\Simulations\World_Building_Project\03_Applications\Map_Viewer\data\master_world_data.json"
WIKI_DIR = r"c:\Proyectos_Local\Software-Development\Simulations\World_Building_Project\03_Applications\Map_Viewer\wiki"
LOG_FILE = r"c:\Proyectos_Local\Software-Development\Simulations\World_Building_Project\03_Applications\Map_Viewer\scripts\force_log.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def update_country_html(country_name, cities):
    filename = country_name.lower().replace(" ", "_") + ".html"
    filepath = os.path.join(WIKI_DIR, "countries", filename)
    
    if not os.path.exists(filepath):
        log(f"⚠️ HTML file not found for {country_name}: {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

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
        ul_end = rest.find("</ul>") + 5 
        
        pre_ul = rest[:ul_start]
        post_ul = rest[ul_end:]

        new_list_items = []
        for city in cities:
            safe_name = city['name'].lower()
            for char in "ýöðæíá":
                safe_name = safe_name.replace(char, "_")
            safe_name = safe_name.replace(" ", "_") + ".html"
            
            new_list_items.append(f'<li><a href="../cities/{safe_name}">{city["name"]}</a> ({city.get("type", "settlement")})</li>')
        
        new_ul = "\n        <ul>" + "".join(new_list_items) + "</ul>"
        
        new_html = pre + pre_ul + new_ul + post_ul
        
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

def force_sync():
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except:
            pass
            
    log("🔄 Force Syncing Wiki HTML...")
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # specifically target Gryning and Oighear first to be sure
        targets = ["Gryning", "Oighear"]
        
        for continent in data.get('continents', []):
            for country in continent.get('countries', []):
                # Update ALL countries just in case, but definitely the targets
                update_country_html(country['name'], country.get('cities', []))

    except Exception as e:
        log(f"❌ Error: {e}")

if __name__ == "__main__":
    force_sync()
