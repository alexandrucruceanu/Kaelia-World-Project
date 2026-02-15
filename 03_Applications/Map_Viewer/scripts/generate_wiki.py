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
/* Dark Theme Variables */
:root {
    --bg-color: #1a1a1a;
    --text-color: #e0e0e0;
    --link-color: #8ab4f8;
    --border-color: #444;
    --header-border: #666;
    --infobox-bg: #2a2a2a;
    --infobox-header: #333;
    --infobox-title-bg: #444;
    --table-header: #333;
    --code-bg: #2d2d2d;
    --blockquote-border: #666;
}

body { font-family: sans-serif; line-height: 1.6; color: var(--text-color); max-width: 1200px; margin: 0 auto; padding: 20px; background: var(--bg-color); }
.header-container { border-bottom: 1px solid var(--header-border); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
h1, h2, h3, h4, h5, h6 { color: #fff; font-family: 'Linux Libertine','Georgia','Times',serif; }
h1 { font-size: 1.8em; margin-bottom: 0.25em; }
h2 { border-bottom: 1px solid var(--header-border); font-size: 1.5em; margin-top: 1.5em; }
h3 { font-size: 1.2em; margin-top: 1.2em; }

.infobox { float: right; width: 300px; background: var(--infobox-bg); border: 1px solid var(--border-color); padding: 10px; margin-left: 20px; font-size: 0.9em; color: var(--text-color); }
.infobox th { text-align: left; background: var(--table-header); padding: 5px; color: #fff; }
.infobox td { padding: 5px; }
.infobox-title { text-align: center; font-weight: bold; font-size: 1.25em; background: var(--infobox-title-bg); padding: 5px; color: #fff; }

.toc { background: var(--infobox-bg); border: 1px solid var(--border-color); display: inline-block; padding: 10px; margin-bottom: 20px; min-width: 200px; }
.toc-title { font-weight: bold; text-align: center; margin-bottom: 5px; }

.section-content { margin-bottom: 20px; }
ul { margin-top: 0; }
a { color: var(--link-color); text-decoration: none; }
a:hover { text-decoration: underline; }

.city-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.city-table th, .city-table td { border: 1px solid var(--border-color); padding: 6px; text-align: left; }
.city-table th { background: var(--table-header); color: #fff; }

.breadcrumb { font-size: 0.8em; color: #aaa; margin-bottom: 10px; }
.hero-img { width: 100%; height: 200px; object-fit: cover; border-radius: 4px; margin-bottom: 10px; border: 1px solid #555; }
.motto { font-style: italic; color: #aaa; text-align: center; display: block; margin-top: 5px; border-top: 1px solid #444; padding-top: 5px; }

/* Scrollbar refinement */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #1a1a1a; }
::-webkit-scrollbar-thumb { background: #555; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #777; }

/* Lightbox/Modal */
.modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.9); }
.modal-content { margin: auto; display: block; width: 80%; max-width: 700px; max-height: 90vh; object-fit: contain; animation-name: zoom; animation-duration: 0.6s; margin-top: 5vh; }
.modal-close { position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; transition: 0.3s; cursor: pointer; }
.modal-close:hover, .modal-close:focus { color: #bbb; text-decoration: none; cursor: pointer; }
.caption { margin: auto; display: block; width: 80%; max-width: 700px; text-align: center; color: #ccc; padding: 10px 0; height: 150px; }
@keyframes zoom { from {transform:scale(0)} to {transform:scale(1)} }
.clickable-img { cursor: pointer; transition: 0.3s; }
.clickable-img:hover { opacity: 0.7; }

/* Wiki Carousel Styles */
.wiki-carousel {
    position: relative;
    width: 100%;
    height: 200px;
    background: var(--infobox-bg);
    overflow: hidden;
    border-radius: 4px;
    margin-bottom: 10px;
}
.wiki-carousel-inner {
    display: flex;
    transition: transform 0.4s ease-in-out;
    height: 100%;
}
.carousel-slide {
    min-width: 100%;
    height: 100%;
    object-fit: cover;
    cursor: pointer;
}
.wiki-carousel-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0,0,0,0.5);
    color: white;
    border: none;
    padding: 8px 12px;
    cursor: pointer;
    z-index: 5;
    border-radius: 4px;
}
.wiki-carousel-btn.prev { left: 5px; }
.wiki-carousel-btn.next { right: 5px; }
.wiki-indicators {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 5px;
}
.wiki-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.5);
    cursor: pointer;
}
.wiki-indicator.active {
    background: white;
}
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
    
    <!-- The Modal -->
    <div id="myModal" class="modal">
      <span class="modal-close" onclick="closeModal()">&times;</span>
      <img class="modal-content" id="img01">
      <div id="caption" class="caption"></div>
    </div>

    <script>
    // Get the modal
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");

    function openModal(src, alt) {{
      modal.style.display = "block";
      modalImg.src = src;
      captionText.innerHTML = alt || "";
    }}

    function closeModal() {{
      modal.style.display = "none";
    }}
    
    // Close on click outside
    window.onclick = function(event) {{
      if (event.target == modal) {{
        modal.style.display = "none";
      }}
    }}
    
    // Wiki Carousel Logic
    var currentWikiSlide = 0;
    function updateWikiCarousel() {{
        var inner = document.getElementById('wiki-carousel-inner');
        if (!inner) return;
        var slides = inner.getElementsByClassName('carousel-slide');
        if (slides.length === 0) return;
        
        if (currentWikiSlide >= slides.length) currentWikiSlide = 0;
        if (currentWikiSlide < 0) currentWikiSlide = slides.length - 1;
        
        inner.style.transform = 'translateX(-' + (currentWikiSlide * 100) + '%)';
        
        var dots = document.getElementsByClassName('wiki-indicator');
        for (var i = 0; i < dots.length; i++) {{
            dots[i].classList.toggle('active', i === currentWikiSlide);
        }}
    }}
    
    function moveWikiSlide(n) {{
        currentWikiSlide += n;
        updateWikiCarousel();
    }}
    
    function setWikiSlide(n) {{
        currentWikiSlide = n;
        updateWikiCarousel();
    }}
    
    // Wiki Generation Functions
    var wikiGenCityId = null;
    var wikiGenType = null;
    
    function wikiGenerate(cityId, genType) {{
        wikiGenCityId = cityId;
        wikiGenType = genType;
        var titles = {{
            'landscape_main': '🖼️ Generate Main (Aerial)',
            'landscape_seq1': '📸 Generate Seq1 (Eye-Level)',
            'landscape_seq2': '🧑‍🏭 Generate Seq2 (Reportage)',
            'heraldry_flag': '🏴 Generate Flag',
            'heraldry_arms': '🛡️ Generate Coat of Arms'
        }};
        document.getElementById('wiki-gen-title').innerText = titles[genType] || 'Generate';
        document.getElementById('wiki-gen-prompt').value = 'Loading prompt...';
        document.getElementById('wiki-gen-prompt').disabled = true;
        document.getElementById('wiki-gen-modal').style.display = 'block';
        var statusEl = document.getElementById('wiki-gen-status');
        statusEl.style.display = 'none';
        document.getElementById('wiki-gen-confirm').disabled = false;
        document.getElementById('wiki-gen-confirm').innerText = '🚀 Generate';
        
        // Get base URL (wiki pages are at /wiki/cities/, server at /)
        var baseUrl = window.location.protocol + '//' + window.location.host;
        
        fetch(baseUrl + '/api/construct-prompt', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ cityId: cityId, genType: genType }})
        }})
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
            document.getElementById('wiki-gen-prompt').value = data.prompt || 'Enter prompt manually.';
            document.getElementById('wiki-gen-prompt').disabled = false;
        }})
        .catch(function(err) {{
            console.error(err);
            document.getElementById('wiki-gen-prompt').value = 'Error loading prompt from server. Please check console logs.';
            document.getElementById('wiki-gen-prompt').disabled = false;
        }});
    }}
    
    function wikiExecuteGeneration() {{
        if (!wikiGenCityId || !wikiGenType) return;
        var prompt = document.getElementById('wiki-gen-prompt').value;
        var model = document.getElementById('wiki-gen-model').value;
        var statusEl = document.getElementById('wiki-gen-status');
        var btn = document.getElementById('wiki-gen-confirm');
        
        statusEl.style.display = 'block';
        statusEl.style.background = '#e8f0fe';
        statusEl.style.color = '#1a73e8';
        statusEl.innerHTML = '⏳ Generating... This may take 15-30 seconds.';
        btn.disabled = true;
        btn.innerText = '⏳ Generating...';
        
        var baseUrl = window.location.protocol + '//' + window.location.host;
        
        fetch(baseUrl + '/api/generate-visual', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                cityId: wikiGenCityId,
                model: model,
                genType: wikiGenType,
                prompt: prompt
            }})
        }})
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
            if (data.status === 'success') {{
                statusEl.style.background = '#e6f4ea';
                statusEl.style.color = '#137333';
                statusEl.innerHTML = '✅ Generated! Reloading page...';
                btn.innerText = '✅ Done';
                setTimeout(function() {{ window.location.reload(); }}, 2000);
            }} else {{
                statusEl.style.background = '#fce8e6';
                statusEl.style.color = '#d93025';
                statusEl.innerHTML = '❌ Error: ' + (data.message || 'Generation failed');
                btn.disabled = false;
                btn.innerText = '🚀 Retry';
            }}
        }})
        .catch(function(err) {{
            statusEl.style.background = '#fce8e6';
            statusEl.style.color = '#d93025';
            statusEl.innerHTML = '❌ Network error: ' + err.message;
            btn.disabled = false;
            btn.innerText = '🚀 Retry';
        }});
    }}
    </script>
</body>
</html>"""

def markdown_to_html(text):
    if not text: return ""
    lines = text.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        # Handle empty lines (reset lists)
        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<br>")
            continue

        # Handle formatting
        # Bold **text**
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        # Italic *text*
        line = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', line)

        # Headers
        if line.startswith('### '):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h3>{line[4:]}</h3>")
            continue
        elif line.startswith('## '):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h2>{line[3:]}</h2>")
            continue
        elif line.startswith('# '):
             if in_list: html_lines.append("</ul>"); in_list = False
             html_lines.append(f"<h1>{line[2:]}</h1>")
             continue

        # Lists (Handle both - and *)
        if line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:]}</li>")
            continue
        
        # Regular text
        if in_list:
            html_lines.append("</ul>")
            in_list = False
        html_lines.append(f"{line}<br>")

    if in_list:
        html_lines.append("</ul>")
        
    return "\n".join(html_lines)

def extract_section(text, section_name):
    pattern = rf'## .*?{re.escape(section_name)}.*?\n(.*?)(?=\n## |$)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def generate_city_page(city, country_name, continent_name):
    slug = slugify(city['name'])
    rel = "../"
    
    # Scan for images - derive directory from city's image path when available
    if city.get('image'):
        # image is like "assets/images/Antarmund/NorKunta/jarnhofn/jarnhofn_main.png"
        img_dir_rel = os.path.dirname(city['image'])
        img_dir_abs = os.path.join(BASE_DIR, img_dir_rel)
    else:
        # Fallback: construct from names
        content_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(WIKI_DIR))))
        def sanitize(text): return "".join(x for x in text if x.isalnum() or x in " _-").strip().replace(" ", "_")
        s_cont = sanitize(continent_name)
        s_country = sanitize(country_name)
        s_city = sanitize(city['name']).lower()
        img_dir_rel = f"assets/images/{s_cont}/{s_country}/{s_city}"
        img_dir_abs = os.path.join(BASE_DIR, img_dir_rel)
    
    found_images = []
    if os.path.exists(img_dir_abs):
        for f in os.listdir(img_dir_abs):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                found_images.append(f"../../{img_dir_rel}/{f}")
    
    # Sort: main, then seq1, then seq2, then others
    def sort_key(x):
        if '_main' in x: return 0
        if '_seq1' in x: return 1
        if '_seq2' in x: return 2
        return 3
    found_images.sort(key=sort_key)
    
    hero_html = ""
    if len(found_images) > 1:
        # Carousel HTML
        slides = "".join([f'<img src="{src}" class="hero-img carousel-slide {"active" if i==0 else ""}" alt="{city["name"]}" onclick="openModal(this.src, \'{city["name"]}\')">' for i, src in enumerate(found_images)])
        dots = "".join([f'<div class="wiki-indicator {"active" if i==0 else ""}" onclick="setWikiSlide({i})"></div>' for i in range(len(found_images))])
        hero_html = f"""
        <div class="wiki-carousel">
            <div class="wiki-carousel-inner" id="wiki-carousel-inner">
                {slides}
            </div>
            <button class="wiki-carousel-btn prev" onclick="moveWikiSlide(-1)">❮</button>
            <button class="wiki-carousel-btn next" onclick="moveWikiSlide(1)">❯</button>
            <div class="wiki-indicators">{dots}</div>
        </div>
        """
    elif len(found_images) == 1:
        hero_html = f'<img src="{found_images[0]}" class="hero-img clickable-img" alt="{city["name"]}" onclick="openModal(this.src, \'{city["name"]}\')">'
    else:
        hero_html = f'<img src="../../{city.get("image", "img/satellite.jpg")}" class="hero-img clickable-img" alt="{city["name"]}" onclick="openModal(this.src, \'{city["name"]}\')">'

    # Heraldry Images
    flag_img = ""
    if city.get('heraldry', {}).get('flag'):
        flag_src = "../../" + city["heraldry"]["flag"].lstrip("/")
        flag_img = f'<img src="{flag_src}" class="clickable-img" style="width:100px; border:1px solid #666; margin: 2px;" title="Flag" onclick="openModal(this.src, \'Flag of {city["name"]}\')">'
    
    arms_img = ""
    if city.get('heraldry', {}).get('coat_of_arms'):
        arms_src = "../../" + city["heraldry"]["coat_of_arms"].lstrip("/")
        arms_img = f'<img src="{arms_src}" class="clickable-img" style="width:80px; border:none; margin: 2px;" title="Coat of Arms" onclick="openModal(this.src, \'Coat of Arms of {city["name"]}\')">'

    infobox = f"""<div class="infobox">
        <div class="infobox-title">{city['name']}</div>
        <table>
            <tr><td colspan="2" style="text-align:center">
                {hero_html}
                <div style="display:flex; justify-content:center; align-items:center; gap:10px; margin-top:5px;">
                    {flag_img}
                    {arms_img}
                </div>
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

    # Generation Buttons
    city_id = city.get('id', '')
    content += f"""
    <h2>Generate Assets</h2>
    <div class="section-content" style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
        <button onclick="wikiGenerate('{city_id}', 'landscape_main')" class="wiki-gen-btn" style="padding: 8px 14px; background: #1a73e8; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">🖼️ Main (Aerial)</button>
        <button onclick="wikiGenerate('{city_id}', 'landscape_seq1')" class="wiki-gen-btn" style="padding: 8px 14px; background: #e37400; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">📸 Seq1 (Eye-Level)</button>
        <button onclick="wikiGenerate('{city_id}', 'landscape_seq2')" class="wiki-gen-btn" style="padding: 8px 14px; background: #d93025; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">🧑‍🏭 Seq2 (Activity)</button>
        <button onclick="wikiGenerate('{city_id}', 'heraldry_flag')" class="wiki-gen-btn" style="padding: 8px 14px; background: #137333; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">🏴 Flag</button>
        <button onclick="wikiGenerate('{city_id}', 'heraldry_arms')" class="wiki-gen-btn" style="padding: 8px 14px; background: #b06000; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem;">🛡️ Arms</button>
    </div>
    <div id="wiki-gen-modal" style="display:none; background: #f8f9fa; border: 1px solid #dadce0; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
        <h3 id="wiki-gen-title" style="margin-top:0; font-size: 1rem;"></h3>
        <label style="font-size: 0.8rem; color: #5f6368; font-weight: 500;">Prompt (editable)</label>
        <textarea id="wiki-gen-prompt" rows="5" style="width: 100%; box-sizing: border-box; font-family: monospace; font-size: 0.8rem; margin-top: 4px; padding: 8px; border: 1px solid #dadce0; border-radius: 4px; resize: vertical;"></textarea>
        <div style="display: flex; gap: 8px; margin-top: 8px; align-items: center;">
            <select id="wiki-gen-model" style="padding: 6px 10px; border: 1px solid #dadce0; border-radius: 4px;">
                <option value="fast">Flash (Fast)</option>
                <option value="pro">Pro (Hifi)</option>
            </select>
            <button id="wiki-gen-confirm" onclick="wikiExecuteGeneration()" style="padding: 8px 16px; background: #1a73e8; color: white; border: none; border-radius: 4px; cursor: pointer;">🚀 Generate</button>
            <button onclick="document.getElementById('wiki-gen-modal').style.display='none'" style="padding: 8px 16px; background: none; border: 1px solid #dadce0; border-radius: 4px; cursor: pointer;">Cancel</button>
        </div>
        <div id="wiki-gen-status" style="margin-top: 8px; font-size: 0.85rem; display: none; padding: 8px; border-radius: 4px;"></div>
    </div>
    """

    html = wrap_html(content, city['name'], depth=1)
    path = os.path.join(WIKI_DIR, 'cities', f"{slug}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_country_page(country, continent_name):
    slug = slugify(country['name'])
    rel = "../"
    
    cities_html = "".join([f'<li><a href="../cities/{slugify(c["name"])}.html">{c["name"]}</a> ({c["type"]})</li>' for c in country['cities']])
    
    # Heraldry Images
    flag_img = ""
    if country.get('heraldry', {}).get('flag'):
        flag_src = "../../" + country["heraldry"]["flag"].lstrip("/")
        flag_img = f'<img src="{flag_src}" class="hero-img clickable-img" alt="Flag of {country["name"]}" style="width:100%; height:auto;" onclick="openModal(this.src, \'Flag of {country["name"]}\')">'
    
    arms_img = ""
    if country.get('heraldry', {}).get('coat_of_arms'):
        arms_src = "../../" + country["heraldry"]["coat_of_arms"].lstrip("/")
        arms_img = f'<div style="text-align:center; margin-top:5px;"><img src="{arms_src}" class="clickable-img" style="width:100px; height:auto;" alt="Coat of Arms" onclick="openModal(this.src, \'Coat of Arms of {country["name"]}\')"></div>'

    infobox = f"""<div class="infobox">
        <div class="infobox-title">{country['name']}</div>
        <table>
            <tr><td colspan="2" style="text-align:center">
                {flag_img}
                {arms_img}
                {f'<div class="motto">"{country["heraldry"]["motto"]}"</div>' if country.get('heraldry', {}).get('motto') else ''}
            </td></tr>
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
            <tr><td colspan="2" style="text-align:center"><img src="../data/altitude_map.jpg" alt="Map of Kaelia" class="clickable-img" style="width:100%" onclick="openModal(this.src, 'Map of Kaelia')"></td></tr>
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
