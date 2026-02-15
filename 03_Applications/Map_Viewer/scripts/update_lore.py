import json
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
MASTER_DATA_FILE = os.path.join(DATA_DIR, 'master_world_data.json')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def update_city_data(cities, target_id, updates):
    for city in cities:
        if city['id'] == target_id:
            print(f"Updating {city['name']} ({target_id})...")
            # Update fields
            if 'desc' in updates: city['desc'] = updates['desc']
            if 'lore' in updates: city['lore'] = updates['lore']
            if 'visual_data' in updates: city['visual_data'] = updates['visual_data']
            if 'heraldry' in updates:
                 # Merge heraldry safely
                 if 'heraldry' not in city: city['heraldry'] = {}
                 city['heraldry'].update(updates['heraldry'])
            return True
    return False

def main():
    data = load_json(MASTER_DATA_FILE)
    count = 0

    # Updates Definition
    updates_map = {
        # --- KASY FEDERATION ---
        "city_15": { # Yokasy (Tropical Evergreen Forest)
            "desc": "Bioluminescent canopy metropolis integrated into massive ancient trees.",
            "lore": {
                "desc": "Yokasy is a marvel of bio-architecture, built not on the ground, but within the massive, hollowed trunks and branches of the Ironwood giants. It is a vertical city of hanging bridges, bioluminescent lighting, and harmonious existence with the dense tropical rainforest.",
                "source": "WORLD_CODEX.md (Updated)"
            },
            "visual_data": {
                "schema": {
                    "meta": {"image_type": "Bio-Architecture", "aspect_ratio": "16:9"},
                    "global_context": {
                        "scene_description": "City built in the canopy of giant trees.",
                        "lighting": "Bioluminescent blue and green glow",
                        "atmosphere": "Humid, mystical, organic"
                    },
                    "composition": {"camera_angle": "Low angle looking up at bridges", "focal_point": "The network of hanging walkways"},
                    "objects": [
                        {"id": "trees", "visual_attributes": {"appearance": "Massive Ironwood trunks", "scale": "Titanic"}},
                        {"id": "structures", "visual_attributes": {"appearance": "Woven living wood pods", "lighting": "Glowing organism"}}
                    ]
                }
            }
        },
        "city_16": { # Vorkasy (Ocean)
            "desc": "Floating solar-grid archipelago protecting a coral reef.",
            "lore": {
                "desc": "Vorkasy consists of interconnected floating platforms and artificial atolls. It harnesses the intense tropical sun while shading the delicate coral reefs below, creating a sanctuary for marine mega-fauna and a hub for aquaponics.",
                "source": "WORLD_CODEX.md (Updated)"
            },
            "visual_data": {
                "schema": {
                    "meta": {"image_type": "Aerial Oceanpunk", "aspect_ratio": "16:9"},
                    "global_context": {
                        "scene_description": "Floating city on a clear tropical ocean.",
                        "lighting": "Bright, harsh tropical sun",
                        "atmosphere": "Clean, futuristic, aquatic"
                    },
                    "composition": {"camera_angle": "High angle aerial", "focal_point": "The geometry of the floating platforms"},
                    "objects": [
                        {"id": "platforms", "visual_attributes": {"appearance": "White hexagonal solar islands", "function": "Floating habitation"}},
                        {"id": "water", "visual_attributes": {"appearance": "Crystal clear turquoise", "content": "Visible coral reefs"}}
                    ]
                }
            }
        },
        "city_17": { # Pomkasy (Tropical Evergreen Forest)
            "desc": "Mangrove cyber-port integrated into the coastal roots.",
            "lore": {
                "desc": "Built into a massive, genetically engineered mangrove forest, Pomkasy is a city that breathes with the tide. Its structures are woven from steel-reinforced root systems, protecting it from tropical storms while serving as a hidden hub for pearl-biotech and synthetic dyes.",
                "source": "WORLD_CODEX.md (Updated)"
            },
            "visual_data": {
                "schema": {
                    "meta": {"image_type": "Biopunk Swamp", "aspect_ratio": "16:9"},
                    "global_context": {
                        "scene_description": "City woven into giant mangrove roots.",
                        "lighting": "Dappled sunlight through dense leaves",
                        "atmosphere": "Humid, protective, hidden"
                    },
                     "composition": {"camera_angle": "Water-level looking into the roots", "focal_point": "A sleek pod nested in the roots"},
                    "objects": [
                        {"id": "architecture", "visual_attributes": {"appearance": "Pod-like structures", "location": "In mangrove roots"}},
                        {"id": "transport", "visual_attributes": {"appearance": "Small silent boats"}}
                    ]
                }
            }
        },
        "city_25": { # NorKunta Prime (Temperate Forest)
            "desc": "Temperate industrial metropolis located in a rare warm-valley microclimate.",
            "lore": {
                "desc": "NorKunta Prime is an anomaly: a colossal industrial sprawl (Pop: 4.2M) located in a geothermally warmed valley. It is the beating heart of the north, where heavy industry meets high-density living. The city is divided into the 'Furnace' industrial zones, the 'Hearth' residential mega-blocks, and the ice-free 'Iron Harbor' that connects it to the frozen sea. It is a place of steam, steel, and unceasing activity.",
                "source": "WORLD_CODEX.md (Updated)"
            },
            "visual_data": {
                "schema": {
                    "meta": {"image_type": "Industrial Metropolis", "aspect_ratio": "16:9"},
                    "global_context": {
                        "scene_description": "Sprawling industrial metropolis (4.2M people) in a steam-filled temperate valley.",
                        "lighting": "Orange industrial haze mixing with grey overcast daylight",
                        "atmosphere": "Bustling, gritty, massive scale, steam vs ice contrast"
                    },
                    "composition": {"camera_angle": "Wide aerial shot from the harbor looking inland", "focal_point": "The transition from the busy harbor to the dense skyscrapers"},
                    "objects": [
                        {"id": "harbor", "visual_attributes": {"appearance": "Massive ice-free deep water port", "activity": "Cargo ships docking, cranes operating"}},
                        {"id": "residential", "visual_attributes": {"appearance": "Endless rows of 'Hearth' mega-blocks", "density": "Extremely high, vertical slums and towers"}},
                        {"id": "commercial", "visual_attributes": {"appearance": "Neon-lit trade districts", "location": "Central valleys between factory zones"}},
                        {"id": "industry", "visual_attributes": {"appearance": "Colossal foundries and smokestacks", "effect": "Generating heat and steam clouds"}}
                    ]
                }
            },
            "heraldry": {
                "description": "A steaming iron gear rising from a glacial blue field."
            }
        },
        "city_18": { # Saskasy (Now Tropical/Forest, was Desert)
            "desc": "Deep jungle research station monitoring biodiversity.",
            "lore": {
                "desc": "Hidden deep within the impenetrable undergrowth, Saskasy is a scientific outpost dedicated to cataloging the planet's most diverse ecosystem. The scientists here live in raised modular habitats to avoid the seasonal floods and predators of the jungle floor.",
                "source": "WORLD_CODEX.md (Updated)"
            },
            "visual_data": {
                "schema": {
                    "meta": {"image_type": "Jungle Expedition", "aspect_ratio": "16:9"},
                    "global_context": {
                        "scene_description": "Research station in deep jungle undergrowth.",
                        "lighting": "Dim, filtered through dense leaves",
                        "atmosphere": "Wet, claustrophobic, discovery"
                    },
                    "composition": {"camera_angle": "Eye-level from the ground", "focal_point": "The lighted window of a lab module"},
                    "objects": [
                        {"id": "structures", "visual_attributes": {"appearance": "Raised modular prefabs", "features": " Covered in moss"}},
                        {"id": "foliage", "visual_attributes": {"appearance": "Dense giant ferns and vines", "weather": "Heavy rain"}}
                    ]
                }
            }
        },
        "city_nk_1": { # Jarnhöfn (Boreal/Alpine)
            "desc": "Sprawling industrial-residential metropolis on a frozen sea with massive naval shipyards.",
            "lore": {
                "desc": "Known as the 'Iron Harbor', Jarnhöfn is the logistical spine of the continent (Pop: 850k). Its nuclear-powered ice-breakers keep the trade lanes open year-round, defying the encroaching pack ice. The city's culture is one of rugged endurance, where every citizen is part of the great engine of commerce, and the docks never sleep.",
                "source": "WORLD_CODEX.md (Updated)"
            },
            "visual_data": {
                "schema": {
                    "meta": {"image_type": "Aerial Cityscape", "aspect_ratio": "4:3"},
                    "global_context": {
                        "scene_description": "Sprawling industrial metropolis (850k pop) on a frozen coast.",
                        "lighting": "Arctic twilight with warm orange city lights and neon signs",
                        "atmosphere": "Bustling, cold, survivalist, heavy"
                    },
                    "composition": {"camera_angle": "High-altitude aerial looking down at the coast", "focal_point": "The contrast between the dark shipyard and the glowing hab-blocks"},
                    "objects": [
                        {"id": "residential", "visual_attributes": {"appearance": "Dense blocky concrete hab-blocks", "lighting": "Warm orange streetlights"}},
                        {"id": "commercial", "visual_attributes": {"appearance": "Neon-lit modular zones near rails", "activity": "Busy markets in snow"}},
                        {"id": "industry", "visual_attributes": {"appearance": "Nuclear naval shipyards", "action": "Cranes constructing ice-breakers to clear the frozen sea"}},
                        {"id": "environment", "visual_attributes": {"appearance": "Frozen sea with thermal wakes", "features": "Jagged ice floes"}}
                    ]
                }
            },
            "heraldry": {
                "description": "A black iron anchor shattering a block of blue ice."
            }
        },
        # --- NORDICA TWEAKS (Example) ---
        "city_1": { # Skýjakot (Confirmed Boreal) - Tweak prompt to emphasize mist/cold
             "visual_data": {
                "schema": {
                  "meta": {
                    "image_type": "Cinematic Photorealism, 8k",
                    "aspect_ratio": "16:9"
                  },
                  "global_context": {
                    "scene_description": "Wide shot of Skýjakot, a city built atop the dense canopy of a dark Boreal forest.",
                    "lighting": "Diffused nordic light, glowing blue energy lines",
                    "atmosphere": "Misty, cold, industrial-natural fusion"
                  },
                  "composition": {
                    "camera_angle": "Wide cinematic shot, slightly elevated",
                    "focal_point": "Aerodynamic wind-turbines rising above the pines"
                  },
                  "objects": [
                    {
                      "id": "architecture",
                      "visual_attributes": {
                        "appearance": "Sleek glass fused with sustainable timber",
                        "action": "Suspended at canopy level"
                      }
                    },
                    {
                      "id": "surroundings",
                      "visual_attributes": {
                        "appearance": "Ancient dark pine forest (Taiga)",
                        "background": "Mist-covered mountains"
                      }
                    }
                  ]
                }
              }
        }
    }

    # APPLY UPDATES
    for continent in data['continents']:
        for country in continent['countries']:
            for city in country['cities']:
                cid = city['id']
                if cid in updates_map:
                    # Merge logic: visuals might be partial, but here we replace specific internal dicts
                    # We use the helper to replace top-level keys if they exist in updates_map[cid]
                    u = updates_map[cid]
                    if 'desc' in u: city['desc'] = u['desc']
                    if 'lore' in u: city['lore'] = u['lore']
                    if 'visual_data' in u: city['visual_data'] = u['visual_data']
                    print(f"Updated {cid}")
                    count += 1
    
    save_json(MASTER_DATA_FILE, data)
    print(f"Total cities updated: {count}")

if __name__ == "__main__":
    main()
