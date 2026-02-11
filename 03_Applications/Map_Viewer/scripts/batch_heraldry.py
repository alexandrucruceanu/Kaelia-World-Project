import json
import os

data_path = 'data/master_world_data.json'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit(1)

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Comprehensive Country Data (40 Countries)
country_heraldry = {
    # Nordica
    'Gryning': {'motto': 'Over the Canopy, Towards the Light', 'desc': 'Deep violet with a silver stylized pine tree.'},
    'Oighear': {'motto': 'Tradition Guarded by the Vault', 'desc': 'Sky blue and stone grey vertical bicolor.'},
    'Keunmor': {'motto': 'Unshakable as the Root of the World', 'desc': 'White with a jagged dark grey horizontal stripe.'},
    'Brechar': {'motto': 'Roots in the East, Breath in the Wind', 'desc': 'Forest green with three golden leaves.'},
    'Kornmor': {'motto': 'Elegance in Every Thread', 'desc': 'Silken white with a gold spindle.'},
    
    # Kasy Federation
    'The Golden Isles': {'motto': 'Sunlight Deep, Roots Wide', 'desc': 'Gold and olive green diagonal bicolor.'},
    'Akasy': {'motto': 'Thirst for Innovation', 'desc': 'Sand beige with a blue drop emblem.'},
    'Bakausy': {'motto': 'Mirage of Progress', 'desc': 'Burnt orange with a shimmering silver horizon line.'},
    'Pomkasy': {'motto': 'Pearls of the Southern Tide', 'desc': 'Iridescent pearl on a deep sea blue field.'},
    'Saskasy': {'motto': 'Dunes that Never Rest', 'desc': 'Ochre field with a stylized wind-swept dune.'},
    'Vorkasy': {'motto': 'Guardian of the Living Pulse', 'desc': 'Emerald green with a pulse-line in gold.'},
    'Yokasy': {'motto': 'Wellspring of the Sand', 'desc': 'Red sandstone color with a central blue circle.'},
    
    # Betereko
    'The Plateau': {'motto': 'The Infinite Watch', 'desc': 'Deep cobalt blue with a single white star.'},
    'Betereko': {'motto': 'Calculated Ascent', 'desc': 'Monolithic grey with a silver upward chevron.'},
    
    # The Mirelands
    'The Dark-Water States': {'motto': 'Where Water Ends, Industry Begins', 'desc': 'Dark teal with a copper gear.'},
    'Ax Pelak Yeldo': {'motto': 'Thriving in the Surge', 'desc': 'Seafoam green with three silver waves.'},
    'Aghaz': {'motto': 'Fortress of the Silent Data', 'desc': 'Black field with a bronze gate.'},
    'Menulys': {'motto': 'Capturing the Carbon, Preserving the Breath', 'desc': 'Moss green with a black circular sink.'},
    'Mesek': {'motto': 'Guiding Light in the Gloom', 'desc': 'Bioluminescent cyan on a dark indigo field.'},
    'Misyats': {'motto': 'Shadowed by the Moon, Lit by Faith', 'desc': 'Silver crescent on a midnight blue field.'},
    'Nechars': {'motto': 'Wardens of the Eternal Frost', 'desc': 'Steel grey with a white frostflake.'},
    'Niruz': {'motto': 'Growth Against the Tide', 'desc': 'Mud brown with a golden sprout rising from water.'},
    'Pateraz': {'motto': 'Vessels of the Flow', 'desc': 'Teal and copper horizontal stripes.'},
    'Redez': {'motto': 'Adaptive, Enduring, Amphibious', 'desc': 'Rust orange with a stylized tread-track.'},
    'Tailaz': {'motto': 'Legacy of the Delta', 'desc': 'Cyan field with silver branching veins.'},
    
    # Antarmund
    'NorKunta': {'motto': 'Forged in the Glacial Dark', 'desc': 'Charcoal grey with a glowing cyan line.'},
    'Southern Prosperity Rim': {'motto': 'Lush Lands, Boundless Wealth', 'desc': 'Rich green with a golden horn of plenty.'},
    "Dirka'Merik": {'motto': 'Commerce through the Storm', 'desc': 'Navy blue with a golden compass.'},
    "Fyny'Dor": {'motto': 'The Endless Harvest', 'desc': 'Amber gold with a stylized wheat stalk.'},
    'Guldhorn': {'motto': 'Digital Sovereignty, Physical Wealth', 'desc': 'Golden field with a black electronic traces.'},
    "Kasim'Merik": {'motto': 'Master of the Eastern Tides', 'desc': 'Deep azure with a white sail.'},
    'Laendamania': {'motto': 'Echoes of the Southern Voice', 'desc': 'Magenta with a silver broadcast icon.'},
    "Meit'Val": {'motto': 'Luxury from the Earth', 'desc': 'Burgundy with a golden vine.'},
    'Melynmania': {'motto': 'Vibrancy in the Deciduous Heart', 'desc': 'Yellow field with a red maple leaf.'},
    'Metsemania': {'motto': 'Synthesis of the Ancient Wood', 'desc': 'Dark forest green with silver nanobots.'},
    'Norgborg': {'motto': 'Shield of the Southern Gate', 'desc': 'Iron grey with a dark green pine bough.'},
    'Norginde': {'motto': 'Heat of the Core, Strength of the Peak', 'desc': 'Crimson with a grey mountain silhouette.'},
    'Norgkes': {'motto': 'Precision in Every Gear', 'desc': 'Silver field with three interlocking gears.'},
    'Sigmarignen': {'motto': 'Artistry of the High Tradition', 'desc': 'Royal purple with a golden laurel.'},
    'Varelmond': {'motto': 'The Alchemical Beacon', 'desc': 'Prismatic white with a glowing orange spark.'}
}

# City Data (Mapping mottos and descriptions for all 74 cities)
city_mottos = {
    # Nordica Cities
    'Skýjakot': ('Above the Clouds, Always Grounded', 'Violet field with a white cloud and silver pine.'),
    'Hafnir': ('Gateway to the North', 'Blue anchor on a silver field.'),
    'Bjarnarfjörður': ('Knowledge from the Peak', 'White peak with a blue sapphire.'),
    'Árbær': ('The Hand that Crafts', 'Green leaf with silver circuits.'),
    'Vík': ('Echoes on the Black Sand', 'Black beach with a white breaking wave.'),
    'Kaldakinn': ('Witnesses of the Ice', 'White glacier on deep blue.'),
    'Blakkar Array': ('Listening to the Void', 'Orange signal tower on dark grey.'),
    'Koldfisk Rig': ('Harvesting the Cold', 'A silver fish skeleton on a black industrial rig.'),
    'Sydgard': ('The South Gate', 'A solid iron gate on a field of white snow.'),
    'Titansmidja': ('Anvil of the Gods', 'A massive hammer striking an icy spark.'),
    'Jarnhofn': ('The Iron Harbor', 'An iron anchor frozen in a blue block of ice.'),
    'Brechar Capital': ('Eastern Watch', 'Golden leaf on a forest green field.'),
    'Kornmor Capital': ('Woven from History', 'Silver spindle on a silken white field.'),
    
    # Kasy Cities
    'Yokasy': ('Under the Light-Well', 'A red sandstone arch with a golden sun filtering down.'),
    'Vorkasy': ('Preserving the Pulse', 'A green gazelle on a solar mirror field.'),
    'Pomkasy': ('Pearls of the Deep', 'An iridescent shell over a biotech flask.'),
    'Saskasy': ('Dunes of Discovery', 'A nomadic tent under a ringed planet sky.'),
    'Akasy Capital': ('Water is Life', 'Blue drop on a sand beige field.'),
    'Bakausy Capital': ('The Oasis Found', 'Silver palm tree on a burnt orange field.'),
    'Pomkasy Capital': ('Jewel of the Gulf', 'Blue iridescent shell on indigo.'),
    'Saskasy Capital': ('Dune Master', 'Stylized golden dune on ochre.'),
    'Vorkasy Capital': ('Heartbeat of the Scrub', 'Golden pulse-line on emerald.'),
    'Yokasy Capital': ('First Light', 'Golden sun rising between red pillars.'),
    
    # Betereko Cities
    'Apex': ('The Infinite Horizon', 'A telescope atop a white cliff.'),
    'Betereko Capital': ('Peak of Precision', 'Silver upward chevron on monolithic grey.'),
    
    # Mirelands Cities
    'Redez': ('Drifting Forward', 'A floating warehouse on a dark teal field.'),
    'Aghaz Capital': ('Guardian of Secrets', 'Bronze gate on a black field.'),
    'Menulys Capital': ('Breathe Deep', 'Black circular sink on moss green.'),
    'Mesek Capital': ('Bioluminescent Heart', 'Cyan glow on dark indigo.'),
    'Misyats Capital': ('Lunar Sentinel', 'Silver crescent on midnight blue.'),
    'Nechars Capital': ('Frost Wall', 'Steel grey field with a white frostflake.'),
    'Niruz Capital': ('Sprout through Storm', 'Golden sprout on mud brown.'),
    'Pateraz Capital': ('Riverflow', 'Teal and copper horizontal stripes.'),
    'Redez Capital': ('Treads of Progress', 'Rust orange field with tread-tracks.'),
    'Tailaz Capital': ('Delta Spirit', 'Silver veins on a cyan field.'),
    'Niruz': ('Grounded and Growing', 'Brown field with vibrant green circuits.'),
    'Aero-Valli': ('Where Winds Whisper', 'A stylized wind turbine with three golden blades.'),
    'Echo Ridge': ('Sounds of the Earth', 'A series of expanding sound waves over a mountain.'),
    'Thermal Springs': ('Heat from the Heart', 'Steam rising from a cleft in the stone.'),
    'Cryo-Vault 09': ('Frozen Wisdom', 'A crystalline vault door on a white field.'),
    'Misyats': ('Night Watch', 'A silver owl on a dark blue field.'),
    'Nechars': ('Silent Snow', 'A white owl flying over a grey forest.'),
    
    # Antarmund Cities
    'NorKunta Prime': ('Heart of the Titan', 'A massive steel gear over a blue glacier.'),
    'Borealis Station': ('Under the Dancing Lights', 'A stylized aurora over a research dome.'),
    'Ice-Hauler\'s Rest': ('Warmth in the Waste', 'A glowing orange lantern on charcoal grey.'),
    'Glacial Edge': ('Standing at the End', 'A lone tower at the edge of a white cliff.'),
    'Metsemania': ('The Great Redwood', 'A giant sequoia tree with silver leaves.'),
    'Sigmarignen': ('Legacy of Art', 'A golden brush crossing a royal purple field.'),
    'Norgborg': ('City of the Eternal Pine', 'A tall, dark green pine tree on a grey shield.'),
    'Dirka\'Merik Capital': ('Safe Harbor', 'Golden compass on navy blue.'),
    'Fyny\'Dor Capital': ('Bountiful Field', 'Amber gold field with a wheat stalk.'),
    'Kasim\'Merik Capital': ('Master Mariner', 'White sail on deep azure.'),
    'Laendamania Capital': ('The Broadcaster', 'Silver antenna on magenta.'),
    'Meit\'Val Capital': ('The Vine of Plenty', 'Golden vine on burgundy.'),
    'Melynmania Capital': ('The Autumn Leaf', 'Red maple leaf on yellow.'),
    'Metsemania Capital': ('Wood and Logic', 'Green shield with a silver circuit-tree.'),
    'Norgborg Capital': ('Iron Pine', 'Dark green pine branch on iron grey.'),
    'Norginde Capital': ('Core Heat', 'Crimson field with a grey mountain silhouette.'),
    'Norgkes Capital': ('Interlocking Strength', 'Three silver gears on a white field.'),
    'Sigmarignen Capital': ('High Tradition', 'Royal purple field with a golden crown.'),
    'Varelmond Capital': ('Alchemical Spark', 'Prismatic white field with an orange ember.'),
    'Guldhorn Capital': ('Wealth in Data', 'Black electronic trace on a gold field.'),
    
    # JSON Key Corrections
    'Jarnh\u00f6fn': ('The Iron Harbor', 'An iron anchor frozen in a blue block of ice.'),
    'Thermal-Springs': ('Heat from the Heart', 'Steam rising from a cleft in the stone.'),
    'Sleet-Watch': ('Eyes in the Storm', 'A grey watchtower amidst driving white sleet.'),
    
    # Generic Fallbacks and Missing Names
    'Central Hub': ('The Meeting Point', 'Black circle on a white field.'),
    'Bakausy': ('Vision of the Sun', 'Orange sun on a sand-colored field.'),
    'Akasy': ('Well of Truth', 'Blue circle on a beige field.'),
    'Pomkasy': ('Shell of Prosperity', 'Iridescent spiral on blue.'),
    'Saskasy': ('Nomad Gate', 'Ochre triangle on a tan field.'),
    'Vorkasy': ('Pulse Guardian', 'Green sine-wave on emerald.'),
    'Aghaz': ('Silence is Gold', 'Gold bar on a black field.'),
    'Menulys': ('The Deep Breath', 'Dark green spiral on moss.'),
    'Mesek': ('Glow of the Bog', 'Cyan star on dark teal.'),
    'Norkunta': ('Titan Spirit', 'Grey fist on a cyan field.'),
    'Guldhorn': ('The Golden Horn', 'Golden horn on a black field.'),
    'Varelmond': ('Light of the South', 'White star on an orange field.'),
    'Dirka Merik Capital': ('Compass Point', 'Silver compass on blue.'), # Handle variant
    'Fyny Dor Capital': ('Harvest Home', 'Golden wheat on amber.'),     # Handle variant
    'Kasim Merik Capital': ('Tiderunner', 'White anchor on azure.'),    # Handle variant
    'Meit Val Capital': ('Rich Harvest', 'Golden clusters on burgundy.'), # Handle variant
    'Dirka\u2019Merik': ('Commerce by the Stars', 'Star and compass on navy.'),
    'Fyny\u2019Dor': ('The Breadbasket', 'Golden scythe on amber.'),
    'Kasim\u2019Merik': ('Sea Sovereign', 'Trident on deep azure.'),
    'Meit\u2019Val': ('Abundance', 'Grapevine on a burgundy field.'),
    'Sigmarignen': ('The Artist\'s Gate', 'Golden brush on purple.')
}

def slugify(text):
    import re
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')

def add_h(obj, name, is_country=False):
    if is_country:
        h = country_heraldry.get(name)
        if not h:
            print(f"Warning: No country data for {name}, using default.")
            h = {'motto': 'Peace and Prosperity', 'desc': 'A simple bicolor field.'}
        prefix = 'country'
    else:
        res = city_mottos.get(name)
        if not res:
            # Try to match variants or normalize
            norm_name = name.replace("'", "").replace("\u2019", "")
            res = city_mottos.get(norm_name)
        
        if not res:
            print(f"Warning: No city data for {name}, using default.")
            res = ('Prosperity and Peace', 'A simple field with a city gear symbol.')
        
        m, d = res
        h = {'motto': m, 'desc': d}
        prefix = 'city'
    
    slug = slugify(name)
    obj['heraldry'] = {
        'motto': h['motto'],
        'description': h['desc'],
        'flag': f'/assets/heraldry/flags/{prefix}_{slug}.png',
        'coat_of_arms': f'/assets/heraldry/arms/{prefix}_{slug}.png'
    }

print("Updating heraldry data...")
for cont in data.get('continents', []):
    for country in cont.get('countries', []):
        add_h(country, country['name'], is_country=True)
        for city in country.get('cities', []):
            add_h(city, city['name'])

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully updated heraldry for {len(country_heraldry)} countries and {len(city_mottos)} cities in {data_path}.")
