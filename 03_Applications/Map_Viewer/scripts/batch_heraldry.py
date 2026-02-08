import json
import os

data_path = 'data/master_world_data.json'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit(1)

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Country Data
country_heraldry = {
    'Gryning': {'motto': 'Over the Canopy, Towards the Light', 'desc': 'Deep violet with a silver stylized pine tree.'},
    'Oighear': {'motto': 'Tradition Guarded by the Vault', 'desc': 'Sky blue and stone grey vertical bicolor.'},
    'Keunmor': {'motto': 'Unshakable as the Root of the World', 'desc': 'White with a jagged dark grey horizontal stripe.'},
    'The Golden Isles': {'motto': 'Sunlight Deep, Roots Wide', 'desc': 'Gold and olive green diagonal bicolor.'},
    'The Plateau': {'motto': 'The Infinite Watch', 'desc': 'Deep cobalt blue with a single white star.'},
    'The Dark-Water States': {'motto': 'Where Water Ends, Industry Begins', 'desc': 'Dark teal with a copper gear.'},
    'Ax Pelak Yeldo': {'motto': 'Thriving in the Surge', 'desc': 'Seafoam green with three silver waves.'},
    'NorKunta': {'motto': 'Forged in the Glacial Dark', 'desc': 'Charcoal grey with a glowing cyan line.'},
    'Norgind-Kas': {'motto': 'Resilience in the Frost', 'desc': 'Frost grey with a dark green pine bough.'}
}

# City Data
city_mottos = {
    'Skýjakot': ('Above the Clouds, Always Grounded', 'Violet field with a white cloud and silver pine.'),
    'Hafnir': ('Gateway to the North', 'Blue anchor on a silver field.'),
    'Bjarnarfjörður': ('Knowledge from the Peak', 'White peak with a blue sapphire.'),
    'Árbær': ('The Hand that Crafts', 'Green leaf with silver circuits.'),
    'Vík': ('Echoes on the Black Sand', 'Black beach with a white breaking wave.'),
    'Kaldakinn': ('Witnesses of the Ice', 'White glacier on deep blue.'),
    'Blakkar Array': ('Listening to the Void', 'Orange signal tower on dark grey.'),
    'Khuruldai': ('Unity in the Tundra', 'Sky blue field with three white tents.'),
    'Chaghan Khan': ('Deep Mines, Deep Wisdom', 'Golden pickaxe on a mountain profile.'),
    'Lahorebaig': ('The Pulse of the Bazaar', 'Silk-patterned field with a digital eye.'),
    'Erdene Zuu': ('Ancient Faith, Infinite Data', 'Golden bell over a circuit board.'),
    'Ardmore': ('Carved from the Bone of the World', 'Stone-carved eagle on a white shield.'),
    'Dún na nGall': ('The Iron Port', 'Sleek iron ship on iron-grey water.'),
    'Baile Átha Cliath': ('Growth in Every Stone', 'A stone bridge between two green banks.'),
    'Yokasy': ('Under the Light-Well', 'A red sandstone arch with a golden sun filtering down.'),
    'Vorkasy': ('Preserving the Pulse', 'A green gazelle on a solar mirror field.'),
    'Pomkasy': ('Pearls of the Deep', 'An iridescent shell over a biotech flask.'),
    'Saskasy': ('Dunes of Discovery', 'A nomadic tent under a ringed planet sky.'),
    'Apex': ('The Infinite Horizon', 'A telescope atop a white cliff.'),
    'Redez': ('Drifting Forward', 'A floating warehouse on a dark teal field.'),
    'Norkunta Prime': ('Heart of the Glacier', 'A massive steel gear over a blue glacier.'),
    'Koldfisk Rig': ('Harvesting the Cold', 'A silver fish skeleton on a black industrial rig.'),
    'Aero-Valli': ('Where Winds Whisper', 'A stylized wind turbine with three golden blades.'),
    'Echo Ridge': ('Sounds of the Earth', 'A series of expanding sound waves over a mountain.'),
    'Thermal Springs': ('Heat from the Heart', 'Steam rising from a cleft in the stone.'),
    'Sydgard': ('The South Gate', 'A solid iron gate on a field of white snow.'),
    'Glacial Edge': ('Standing at the End', 'A lone tower at the edge of a white cliff.'),
    'Borealis Station': ('Under the Dancing Lights', 'A stylized aurora over a research dome.'),
    'Titansmidja': ('Anvil of the Gods', 'A massive hammer striking an icy spark.'),
    'Jarnhofn': ('The Iron Harbor', 'An iron anchor frozen in a blue block of ice.'),
    'Cryo-Vault 09': ('Frozen Wisdom', 'A crystalline vault door on a white field.'),
    'Norgborg': ('City of the Eternal Pine', 'A tall, dark green pine tree on a grey shield.')
}

def add_h(obj, name, is_country=False):
    if is_country:
        h = country_heraldry.get(name, {'motto': 'Peace and Prosperity', 'desc': 'A simple bicolor field.'})
        prefix = 'country'
    else:
        m, d = city_mottos.get(name, ('Prosperity and Peace', 'A simple field with a city gear symbol.'))
        h = {'motto': m, 'desc': d}
        prefix = 'city'
    
    clean_name = name.lower().replace(' ', '_')
    obj['heraldry'] = {
        'motto': h['motto'],
        'description': h['desc'],
        'flag': f'/assets/heraldry/flags/{prefix}_{clean_name}.png',
        'coat_of_arms': f'/assets/heraldry/arms/{prefix}_{clean_name}.png'
    }

for cont in data.get('continents', []):
    for country in cont.get('countries', []):
        add_h(country, country['name'], is_country=True)
        for city in country.get('cities', []):
            add_h(city, city['name'])

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Successfully updated heraldry for all countries and cities.")
