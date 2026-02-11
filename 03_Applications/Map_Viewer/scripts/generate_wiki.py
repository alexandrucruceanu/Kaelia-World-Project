import json
import os
import re
import shutil

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'master_world_data.json')
CODEX_FILE = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'WORLD_CODEX.md')
WIKI_DIR = os.path.join(BASE_DIR, 'wiki')

# Design Tokens (Wikipedi-esque)
CSS = """
body { font-family: sans-serif; line-height: 1.6; color: #202122; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f6f6f6; }
.header-container { border-bottom: 1px solid #a2a9b1; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
h1 { font-family: 'Linux Libertine','Georgia','Times',serif; font-size: 1.8em; margin-bottom: 0.25em; }
h2 { border-bottom: 1px solid #a2a9b1; font-family: 'Linux Libertine','Georgia','Times',serif; font-size: 1.5em; margin-top: 1.5em; }
h3 { font-size: 1.2em; margin-top: 1.2em; }
.infobox { float: right; width: 300px; background: #f8f9fa; border: 1px solid #a2a9b1; padding: 10px; margin-left: 20px; font-size: 0.9em; }
.infobox th { text-align: left; background: #eaecf0; padding: 5px; }
.infobox td { padding: 5px; }
.infobox-title { text-align: center; font-weight: bold; font-size: 1.25em; background: #cedff2; padding: 5px; }
.toc { background: #f8f9fa; border: 1px solid #a2a9b1; display: inline-block; padding: 10px; margin-bottom: 20px; min-width: 200px; }
.toc-title { font-weight: bold; text-align: center; margin-bottom: 5px; }
.section-content { margin-bottom: 20px; }
ul { margin-top: 0; }
a { color: #0645ad; text-decoration: none; }
a:hover { text-decoration: underline; }
.city-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.city-table th, .city-table td { border: 1px solid #a2a9b1; padding: 6px; text-align: left; }
.city-table th { background: #eaecf0; }
.breadcrumb { font-size: 0.8em; color: #72777d; margin-bottom: 10px; }
.hero-img { width: 100%; height: 200px; object-fit: cover; border-radius: 4px; margin-bottom: 10px; border: 1px solid #dadce0; }
.motto { font-style: italic; color: #555; text-align: center; display: block; margin-top: 5px; border-top: 1px solid #eee; padding-top: 5px; }
"""

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')

def get_rel_path(depth):
    return "../" * depth

def wrap_html(content, title, depth=0):
    rel = get_rel_path(depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - KaeliaWiki</title>
    <style>{CSS}</style>
</head>
<body>
    <div class="breadcrumb">
        <a href="{rel}index.html">Kaelia</a> {' > ' if depth > 0 else ''} {title if depth > 0 else ''}
    </div>
    <div class="header-container">
        <div>
            <h1>{title}</h1>
            <div>From KaeliaWiki, the free encyclopedia</div>
        </div>
        <div style="font-size: 0.9em;"><a href="{rel}../index.html">← Back to Map</a></div>
    </div>
    {content}
</body>
</html>"""

def markdown_to_html(text):
    if not text: return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'^- (.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    text = text.replace('\n', '<br>')
    return text

def extract_section(text, section_name):
    pattern = rf'## .*?{re.escape(section_name)}.*?\n(.*?)(?=\n## |$)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def generate_city_page(city, country_name, continent_name):
    slug = slugify(city['name'])
    rel = "../"
    
    infobox = f"""<div class="infobox">
        <div class="infobox-title">{city['name']}</div>
        <table>
            <tr><td colspan="2" style="text-align:center">
                <img src="../../{city.get('image', 'img/satellite.jpg')}" class="hero-img" alt="{city['name']}">
                {f'<img src="../../{city["heraldry"]["flag"].lstrip("/")}" style="width:100px; border:1px solid #ccc;">' if city.get('heraldry', {}).get('flag') else ''}
                {f'<div class="motto">"{city["heraldry"]["motto"]}"</div>' if city.get('heraldry', {}).get('motto') else ''}
            </td></tr>
            <tr><th>Continent</th><td><a href="../continents/{slugify(continent_name)}.html">{continent_name}</a></td></tr>
            <tr><th>Country</th><td><a href="../countries/{slugify(country_name)}.html">{country_name}</a></td></tr>
            <tr><th>Type</th><td>{city['type'].capitalize()}</td></tr>
            <tr><th>Population</th><td>{city.get('population', 'Unknown')}</td></tr>
            <tr><th>Altitude</th><td>{city.get('altitude', 'Unknown')}</td></tr>
            <tr><th>Climate</th><td>{city.get('biome', 'Unknown')}</td></tr>
            <tr><th>Coordinates</th><td>{city['coords']}</td></tr>
        </table>
    </div>"""

    content = f"""
    {infobox}
    <div class="section-content">
        <p><b>{city['name']}</b> is a {city['type']} located in <a href="../countries/{slugify(country_name)}.html">{country_name}</a>, <a href="../continents/{slugify(continent_name)}.html">{continent_name}</a>. It is situated at an altitude of {city.get('altitude', 'N/A')} and is characterized by a {city.get('biome', 'varied')} climate.</p>
        <h3>Description</h3>
        <p>{city.get('desc', 'No detailed description available.')}</p>
    </div>
    """
    
    if city.get('lore', {}).get('desc'):
        content += f"""<h2>History & Lore</h2><div class="section-content">{markdown_to_html(city['lore']['desc'])}</div>"""

    if city.get('visual_data', {}).get('prompt'):
        content += f"""<h2>Visual Profile</h2><div class="section-content"><p><i>"{city['visual_data']['prompt']}"</i></p></div>"""

    html = wrap_html(content, city['name'], depth=1)
    path = os.path.join(WIKI_DIR, 'cities', f"{slug}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_country_page(country, continent_name):
    slug = slugify(country['name'])
    rel = "../"
    
    cities_html = "".join([f'<li><a href="../cities/{slugify(c["name"])}.html">{c["name"]}</a> ({c["type"]})</li>' for c in country['cities']])
    
    infobox = f"""<div class="infobox">
        <div class="infobox-title">{country['name']}</div>
        <table>
            {f'<tr><td colspan="2" style="text-align:center"><img src="../../{country["heraldry"]["flag"].lstrip("/")}" class="hero-img" alt="Flag of {country["name"]}"><div class="motto">"{country["heraldry"]["motto"]}"</div></td></tr>' if country.get('heraldry', {}).get('flag') else ''}
            <tr><th>Continent</th><td><a href="../continents/{slugify(continent_name)}.html">{continent_name}</a></td></tr>
            <tr><th>Cities</th><td>{len(country['cities'])}</td></tr>
        </table>
    </div>"""

    content = f"""
    {infobox}
    <div class="section-content">
        <p><b>{country['name']}</b> is a sovereign nation on the continent of <a href="../continents/{slugify(continent_name)}.html">{continent_name}</a>.</p>
    </div>
    <h2>Administrative Divisions</h2>
    <div class="section-content">
        <h3>Major Cities</h3>
        <ul>{cities_html}</ul>
    </div>
    """
    
    html = wrap_html(content, country['name'], depth=1)
    path = os.path.join(WIKI_DIR, 'countries', f"{slug}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_continent_page(continent, codex_text):
    slug = slugify(continent['name'])
    rel = "../"
    
    countries_html = "".join([f'<li><a href="../countries/{slugify(c["name"])}.html">{c["name"]}</a></li>' for c in continent['countries']])
    
    lore = extract_section(codex_text, continent['name'])
    
    infobox = f"""<div class="infobox">
        <div class="infobox-title">{continent['name']}</div>
        <table>
            <tr><th>Countries</th><td>{len(continent['countries'])}</td></tr>
        </table>
    </div>"""

    content = f"""
    {infobox}
    <div class="section-content">
        <p><b>{continent['name']}</b> is one of the major landmasses of Kaelia.</p>
        {markdown_to_html(lore)}
    </div>
    <h2>Geopolitics</h2>
    <div class="section-content">
        <ul>{countries_html}</ul>
    </div>
    """
    
    html = wrap_html(content, continent['name'], depth=1)
    path = os.path.join(WIKI_DIR, 'continents', f"{slug}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_index(world_data, codex_text):
    rel = ""
    
    continents_html = ""
    for cont in world_data['continents']:
        continents_html += f'<h3><a href="continents/{slugify(cont["name"])}.html">{cont["name"]}</a></h3>'
        continents_html += "<ul>"
        for country in cont['countries']:
            continents_html += f'<li><a href="countries/{slugify(country["name"])}.html">{country["name"]}</a></li>'
        continents_html += "</ul>"

    infobox = f"""<div class="infobox">
        <div class="infobox-title">Kaelia</div>
        <table>
            <tr><td colspan="2" style="text-align:center"><img src="../data/altitude_map.jpg" alt="Map of Kaelia" style="width:100%"></td></tr>
            <tr><th>Type</th><td>Terrestrial</td></tr>
            <tr><th>Star</th><td>G-type</td></tr>
            <tr><th>Orbit</th><td>1.1 AU</td></tr>
            <tr><th>Year Length</th><td>380 days</td></tr>
            <tr><th>Tech Level</th><td>Information Age</td></tr>
        </table>
    </div>"""

    cosmology = extract_section(codex_text, "Cosmology & Global Physics")

    content = f"""
    {infobox}
    <p><b>Kaelia</b> is an Earth-like terrestrial planet situated at 1.1 AU from its parent G-type star. It is characterized by active tectonics, a diverse range of biomes, and a sophisticated global society.</p>
    
    <h2>Geography</h2>
    <div class="section-content">
        <p>The planet consists of five primary continents, each with unique environmental and cultural characteristics.</p>
        {continents_html}
    </div>

    <h2>Cosmology</h2>
    <div class="section-content">
        {markdown_to_html(cosmology)}
    </div>
    """
    
    html = wrap_html(content, "Main Page", depth=0)
    path = os.path.join(WIKI_DIR, "index.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    # Setup directories
    if os.path.exists(WIKI_DIR):
        shutil.rmtree(WIKI_DIR)
    os.makedirs(WIKI_DIR)
    os.makedirs(os.path.join(WIKI_DIR, 'continents'))
    os.makedirs(os.path.join(WIKI_DIR, 'countries'))
    os.makedirs(os.path.join(WIKI_DIR, 'cities'))

    # Load data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        world_data = json.load(f)
    with open(CODEX_FILE, 'r', encoding='utf-8') as f:
        codex_text = f.read()

    # Generate everything
    generate_index(world_data, codex_text)
    
    for continent in world_data['continents']:
        generate_continent_page(continent, codex_text)
        for country in continent['countries']:
            generate_country_page(country, continent['name'])
            for city in country['cities']:
                generate_city_page(city, country['name'], continent['name'])

    print(f"Full multi-page wiki generated in: {WIKI_DIR}")

if __name__ == "__main__":
    main()
