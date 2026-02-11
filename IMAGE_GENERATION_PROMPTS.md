# 🎨 Image Generation Prompts: Kaelia Modern-Ancient Synthesis

This library provides high-fidelity prompts for the **Information Age** of Kaelia. The aesthetic is **"Modern-Ancient Synthesis"**: 21st-century technology fused with deep ancestral traditions and regional aesthetics.

---

## 🏔️ Continent 1: Nordica
**Theme:** Neo-Nordic, Frigid-Industrial, Boreal/Taiga fusion.

### 1. Gryning (The Wind Coast & Skýjakot)
> *Prompt:* Wide cinematic shot of Skýjakot, a city built atop the dense canopy of a dark Boreal forest (Taiga). Architecture features a fusion of sleek glass and sustainable timber. Massive aerodynamically carved smart-wind-turbines rise above the ancient pine line into the high-altitude laminar flow. Glowing blue energy lines run through the canopy-level streets. Mist-covered mountains in the background. Ultra-realistic, 8k.

```json
{
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
```

### 2. Oighear (The Frost-Lands)
> *Prompt:* A sprawling low-profile city on the icy Alpine Tundra. Buildings resemble traditional nomadic yurts but constructed from curved white composites and interactive solar-glass. High-tech pastoral drones circling above herds of Reindeer and Muskox on the permafrost plain. High-speed rail link elevated on heat-sinking pylons. Sunset over the golden-white steppe.

```json
{
  "meta": {
    "image_type": "Cinematic Photorealism",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "A sprawling low-profile city on the icy Alpine Tundra.",
    "lighting": "Sunset over the golden-white steppe",
    "atmosphere": "Cold, expansive, high-tech pastoral"
  },
  "composition": {
    "camera_angle": "Aerial/Drone high-angle",
    "focal_point": "The mix of yurt-like structures and rail lines"
  },
  "objects": [
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Curved white composites and solar-glass",
        "style": "Neo-Yurt"
      }
    },
    {
      "id": "drones",
      "visual_attributes": {
        "action": "Circling above herds",
        "appearance": "High-tech pastoral drones"
      }
    },
    {
      "id": "infrastructure",
      "visual_attributes": {
        "appearance": "High-speed rail on heat-sinking pylons"
      }
    }
  ]
}
```

### 3. Keunmor (The Iron Peaks)
> *Prompt:* A vertical megacity carved into a jagged Glacial mountain peak. Massive external glass elevators climbing rock faces covered in ice. Internally lit terraced gardens protected by thermal-shields. Steam rising from deep geothermal vents, the primary energy source. Industrial but elegant wood-and-steel finish.

```json
{
  "meta": {
    "image_type": "Architectural Visualization",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "A vertical megacity carved into a jagged Glacial mountain peak.",
    "lighting": "Internal warm garden lights vs cold external ice",
    "atmosphere": "Industrial, hardy, steamy"
  },
  "composition": {
    "camera_angle": "Low angle looking up the mountain",
    "focal_point": "Glass elevators climbing the rock face"
  },
  "objects": [
    {
      "id": "city_structure",
      "visual_attributes": {
        "appearance": "Industrial wood-and-steel finish",
        "features": "Terraced gardens with thermal-shields"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Glacial ice, jagged rock",
        "effect": "Steam rising from geothermal vents"
      }
    }
  ]
}
```

### 4. Brechar (Forest Heart)
> *Prompt:* Dark Boreal forests (Taiga) integrated with modular timber farmsteads. Automated agricultural drones specialized for cold-crops hovering over bioluminescent fields. Smart-grid lines pulsing gently through the dense coniferous canopy. Atmospheric morning mist.

```json
{
  "meta": {
    "image_type": "Atmospheric Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Dark Boreal forests integrated with modular timber farmsteads.",
    "lighting": "Morning mist with pulsing smart-grid lines",
    "atmosphere": "Quiet, technological agrarian"
  },
  "composition": {
    "camera_angle": "Eye-level through the trees",
    "focal_point": "Agricultural drones over bioluminescent fields"
  },
  "objects": [
    {
      "id": "drones",
      "visual_attributes": {
        "appearance": "Automated agricultural units",
        "action": "Hovering over crops"
      }
    },
    {
      "id": "forest",
      "visual_attributes": {
        "appearance": "Dense coniferous canopy",
        "features": "Bioluminescent crops beneath"
      }
    }
  ]
}
```

### 5. Kornmor (Temperate Coast)
> *Prompt:* Oceanic temperate smart city with white stone and hanging gardens, overlooking a high-tech naval trade hub. Cool, lush greenery and misty hills. Sleek white yachts with solar-sails in the harbor. Terraced architecture reflecting the silver sunlight.

```json
{
  "meta": {
    "image_type": "Architectural Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Oceanic temperate smart city overlooking a naval hub.",
    "lighting": "Silver sunlight reflecting off water and white stone",
    "atmosphere": "Clean, wealthy, cosmopolitan"
  },
  "composition": {
    "camera_angle": "Overlooking the harbor",
    "focal_point": "Terraced white architecture and solar-sail yachts"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "White stone, hanging gardens",
        "style": "Terraced"
      }
    },
    {
      "id": "vessels",
      "visual_attributes": {
        "appearance": "Sleek white yachts with solar-sails"
      }
    }
  ]
}
```

### 6. Blakkar (The Echo Island)
> *Prompt:* An eerie, mist-shrouded island in the North Sea. Features a massive, towering automated signal array made of dark, weathered steel. Glowing orange status lights blinking through the fog. Waves crashing against jagged black cliffs.

```json
{
  "meta": {
    "image_type": "Cinematic Mood Piece",
    "aspect_ratio": "21:9"
  },
  "global_context": {
    "scene_description": "An eerie, mist-shrouded island with a massive signal array.",
    "lighting": "Gloomy fog, blinking orange status lights",
    "atmosphere": "Haunted, industrial, lonely"
  },
  "composition": {
    "camera_angle": "Wide shot from the sea",
    "focal_point": "The towering weathered steel array"
  },
  "objects": [
    {
      "id": "structure",
      "visual_attributes": {
        "appearance": "Dark weathered steel tower",
        "features": "Glowing orange lights"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Jagged black cliffs",
        "action": "Waves crashing"
      }
    }
  ]
}
```

---

## ☀️ Continent 2: The Kasy Federation
**Theme:** Mediterranean / Chaparral Solarpunk, Scrubland-Modern, Fire-Resistant Architecture.

### 1. Yokasy (The Under-City)
> *Prompt:* A cross-section of a subterranean metropolis in a rolling Chaparral scrubland. Massive geometric light-wells carved through red sandstone. Surface area dominated by olive and cork agriculture. MAGLEV trains gliding through glass tubes beneath the fire-resistant city shell.

```json
{
  "meta": {
    "image_type": "Architectural Cutaway",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Cross-section of a subterranean metropolis in a rolling scrubland.",
    "lighting": "Natural light filtering down massive shafts",
    "atmosphere": "Cool, protected, bustling"
  },
  "composition": {
    "camera_angle": "Cutaway or looking down a light-well",
    "focal_point": "The MAGLEV trains gliding in glass tubes"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Red sandstone carved geometric wells",
        "features": "Subterranean levels"
      }
    },
    {
      "id": "surface",
      "visual_attributes": {
        "appearance": "Olive and cork agriculture"
      }
    }
  ]
}
```

### 2. Akasy (Solar Spires)
> *Prompt:* A city of slender, mirrored pillars in the golden scrubland. Surface reflects the chaparral vegetation and intense summer sun. Buildings feature active-cooling ceramic facades and automated misting systems for the fire season. Sharp shadows, high contrast, sapphire sky.

```json
{
  "meta": {
    "image_type": "Photorealistic Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "A city of slender, mirrored pillars in the golden scrubland.",
    "lighting": "Intense summer sun, sharp shadows, sapphire sky",
    "atmosphere": "Hot, blindingly bright, pristine"
  },
  "composition": {
    "camera_angle": "Eye-level from the scrubland",
    "focal_point": "Mirrored pillars reflecting the vegetation"
  },
  "objects": [
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Slender mirrored pillars, ceramic facades",
        "features": "Automated misting systems"
      }
    }
  ]
}
```

### 3. Bakausy (Scrubland Hub)
> *Prompt:* Elevated modular city modules standing above a Mediterranean savanna. Architecture blends traditional adobe aesthetics with smart-ceramic fire-proofing. Sky-lions (aerostat drones) patrolling the thermals above olive groves.

```json
{
  "meta": {
    "image_type": "Concept Art",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Elevated modular city modules standing above a Mediterranean savanna.",
    "lighting": "Warm mediterranean light",
    "atmosphere": "Dry, breezy, traditional-futurist"
  },
  "composition": {
    "camera_angle": "Low angle",
    "focal_point": "Elevated modules on stilts"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Adobe aesthetics with smart-ceramic",
        "position": "Elevated"
      }
    },
    {
      "id": "drones",
      "visual_attributes": {
        "appearance": "Sky-lions (aerostat drones)",
        "action": "Patrolling thermals"
      }
    }
  ]
}
```

### 4. Vorkasy (The Solar Sea)
> *Prompt:* A high-tech city surrounded by a massive "Solar Sea" of mirrors harvesting intense UV. The arrays provide shade for chaparral agriculture (vineyards and olives) underneath. Buildings feature white-ceramic outer shells. Digital mirages shimmering on the hot horizon.

```json
{
  "meta": {
    "image_type": "Aerial Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "High-tech city surrounded by a massive field of mirrors.",
    "lighting": "Harsh bright sunlight, digital mirages",
    "atmosphere": "Technological, hot, shimmering"
  },
  "composition": {
    "camera_angle": "High angle aerial",
    "focal_point": "The grid of mirrors protecting the crops"
  },
  "objects": [
    {
      "id": "infrastructure",
      "visual_attributes": {
        "appearance": "See of mirrors/solar arrays",
        "function": "Shading agriculture"
      }
    },
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "White-ceramic outer shells"
      }
    }
  ]
}
```

### 5. Pomkasy (Pearl Coast)
> *Prompt:* A coastal smart-port with architecture inspired by iridescent seashells. Sleek piers extending into a shimmering Mediterranean blue ocean. Biotechnology labs integrated into the coral-reef harbor. Fire-resistant misting towers along the boardwalk.

```json
{
  "meta": {
    "image_type": "Coastal Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Coastal smart-port with iridescent seashell architecture.",
    "lighting": "Bright, shimmering ocean reflection",
    "atmosphere": "Fresh, aquatic, wealthy"
  },
  "composition": {
    "camera_angle": "From the water looking at the piers",
    "focal_point": "The iridescent shell-like buildings"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Iridescent seashell shapes",
        "features": "Fire-resistant misting towers"
      }
    },
    {
      "id": "water",
      "visual_attributes": {
        "appearance": "Shimmering Mediterranean blue",
        "features": "Coral-reef harbor labs"
      }
    }
  ]
}
```

### 6. Saskasy (The Golden Erg)
> *Prompt:* A remote scientific research outpost on the edge of the scrubland and deep dunes. Modular domes featuring advanced atmospheric water generators and sand-storm buffers. Starry night sky with the planetary rings visible.

```json
{
  "meta": {
    "image_type": "Night Sci-Fi Photography",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Remote research outpost on the edge of deep dunes.",
    "lighting": "Starry night sky, planetary rings visible",
    "atmosphere": "Isolated, scientific, cosmic"
  },
  "composition": {
    "camera_angle": "Wide shot showing the isolation",
    "focal_point": "Modular domes glowing in the dark"
  },
  "objects": [
    {
      "id": "structures",
      "visual_attributes": {
        "appearance": "Modular domes",
        "features": "Atmospheric water generators"
      }
    },
    {
      "id": "sky",
      "visual_attributes": {
        "appearance": "Starry with visible planetary rings"
      }
    }
  ]
}
```

---

## ⛰️ Continent 3: Betereko
**Theme:** Technocratic Aerospace, High-Altitude Brutalism, Quantum Grids.

### 1. Apex (The High-Altitude Observatory)
> *Prompt:* Wide cinematic shot of Apex, a city of dignified stone and glass architecture perched on the precipice of a massive sub-polar monolithic plateau. The skyline is dominated by massive modern radio-dish arrays and sleek telecommunications towers overlooking a sheer cliff edge. Clear, thin high-altitude atmosphere with a deep blue sky. Soft sunlight reflecting off glass facades. The "Endless Drop" cliff face falling away into a misty ocean below. Contemporary Information Age aesthetic.

```json
{
  "meta": {
    "image_type": "Cinematic Wide Shot",
    "aspect_ratio": "21:9"
  },
  "global_context": {
    "scene_description": "Apex, a city parked on the precipice of a massive plateau.",
    "lighting": "Clear, thin high-altitude sunlight",
    "atmosphere": "Thin air, vertigo-inducing, scientific"
  },
  "composition": {
    "camera_angle": "Wide cinematic shot",
    "focal_point": "Radio-dish arrays overlooking the drop"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Dignified stone and glass",
        "style": "High-altitude brutalism"
      }
    },
    {
      "id": "infrastructure",
      "visual_attributes": {
        "appearance": "Massive radio-dishes",
        "features": "Telecommunications towers"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "The 'Endless Drop' cliff face",
        "background": "Misty ocean far below"
      }
    }
  ]
}
```

---

## ⚔️ Continent 4: The Mirelands
**Theme:** Cyber-Slavic, Cold Taiga / Sub-Arctic Swamp (Muskeg), Bio-luminescent Organic-Tech.

### 1. Niruz (Smart Crops)
> *Prompt:* Half-frozen flooded Boreal floor with robotic planters. Modular labs on stilts connected by fiber-optic bridges glowing with soft blue light. Dark Taiga forest background with dense pine canopy blocking the sunlight.

```json
{
  "meta": {
    "image_type": "Environmental Concept",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Half-frozen flooded Boreal floor with robotic planters.",
    "lighting": "Soft blue glow from fiber-optics, low natural light",
    "atmosphere": "Damp, cold, glowing"
  },
  "composition": {
    "camera_angle": "Low angle near water surface",
    "focal_point": "Modular labs on stilts"
  },
  "objects": [
    {
      "id": "structures",
      "visual_attributes": {
        "action": "Standing on stilts",
        "features": "Fiber-optic bridges"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Flooded Pine forest",
        "features": "Robotic planters"
      }
    }
  ]
}
```

### 2. Tailas (Delta Hub)
> *Prompt:* A water-city built on a sub-arctic swampy delta. Sleek hydro-skiffs navigating narrow canals through half-frozen water, lined with carved wooden buildings and neon runic signs. Multi-story stilt-architecture.

```json
{
  "meta": {
    "image_type": "Cyberpunk/Folk Fusion",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Water-city on a swampy delta with hydro-skiffs.",
    "lighting": "Neon runic signs reflecting in water",
    "atmosphere": "Travel, trade, mysterious"
  },
  "composition": {
    "camera_angle": "Eye-level from a canal",
    "focal_point": "Hydro-skiff navigating a narrow canal"
  },
  "objects": [
    {
      "id": "vehicle",
      "visual_attributes": {
        "appearance": "Sleek hydro-skiff",
        "action": "Navigating canal"
      }
    },
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Carved wood with neon runes",
        "style": "Stilt-architecture"
      }
    }
  ]
}
```

### 3. Aghaz (Peak Vaults)
> *Prompt:* Fortress-cities built on jagged marsh-peaks above the muskeg. Architecture features dark stone and internal fiber-optic cooling. Defensive energy shields visible as a faint shimmer. Global data vaults hidden beneath the dense arctic mist.

```json
{
  "meta": {
    "image_type": "Matte Painting",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Fortress-cities built on jagged marsh-peaks.",
    "lighting": "Faint shimmer of energy shields, dense mist",
    "atmosphere": "Defensive, secure, hidden"
  },
  "composition": {
    "camera_angle": "Long shot establishing scale",
    "focal_point": "The fortress atop the peak"
  },
  "objects": [
    {
      "id": "fortress",
      "visual_attributes": {
        "appearance": "Dark stone",
        "features": "Energy shields, fiber-optic cooling"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Jagged peaks rising from muskeg"
      }
    }
  ]
}
```

### 4. Pateraz (The River State)
> *Prompt:* A high-density corridor city along a massive black-water river through a flooded forest. Industrial barge-trains powered by bio-gas. Massive water-reclamation plants glowing in the permanent sub-arctic twilight.

```json
{
  "meta": {
    "image_type": "Industrial Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "High-density corridor city along a massive black-water river.",
    "lighting": "Permanent sub-arctic twilight, glowing plants",
    "atmosphere": "Industrial, heavy, flowing"
  },
  "composition": {
    "camera_angle": "Wide shot of the river",
    "focal_point": "Industrial barge-trains"
  },
  "objects": [
    {
      "id": "transport",
      "visual_attributes": {
        "appearance": "Industrial barge-trains",
        "power": "Bio-gas"
      }
    },
    {
      "id": "infrastructure",
      "visual_attributes": {
        "appearance": "Water-reclamation plants",
        "action": "Glowing"
      }
    }
  ]
}
```

### 5. Misyats (The Moon Theocracy)
> *Prompt:* A high-tech city in dark sub-arctic wetlands. Architecture features giant silver lunar motifs and bio-luminescent fiber-optics running through dark wood and stone buildings. Slavic patterns integrated into digital displays. Silver moonlight over a frozen swamp.

```json
{
  "meta": {
    "image_type": "Fantasy/Sci-Fi Fusion",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "High-tech city in wetlands with lunar motifs.",
    "lighting": "Silver moonlight, bio-luminescence",
    "atmosphere": "Sacred, technological, silent"
  },
  "composition": {
    "camera_angle": "Looking up at a building",
    "focal_point": "Giant silver lunar motif on a building"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Dark wood and stone",
        "features": "Silver lunar motifs, Slavic patterns"
      }
    }
  ]
}
```

### 6. Mesek (Biolumin-Labs)
> *Prompt:* A flooded Boreal forest city where the coniferous trees are integrated with fiber-optic networks. Buildings are woven from living vines and glass. Fungal clusters acting as bioluminescent streetlamps in the perpetual gloom.

```json
{
  "meta": {
    "image_type": "Macro/Detail Shot",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Flooded forest city woven from living vines and glass.",
    "lighting": "Gloom illuminated by fungal clusters",
    "atmosphere": "Organic, damp, living"
  },
  "composition": {
    "camera_angle": "Close street level",
    "focal_point": "Fungal clusters acting as streetlamps"
  },
  "objects": [
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Woven vines and glass",
        "features": "Integrated fiber-optics"
      }
    },
    {
      "id": "lighting",
      "visual_attributes": {
        "appearance": "Bioluminescent fungal clusters"
      }
    }
  ]
}
```

### 7. Menulys (The Carbon Sink)
> *Prompt:* A sub-arctic bog region featuring massive fans and carbon-sequestration towers. Industrial but green, with moss-covered machinery and solar-heating networks for permafrost stabilization.

```json
{
  "meta": {
    "image_type": "Industrial Sci-Fi",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Sub-arctic bog featuring massive fans and sequestration towers.",
    "lighting": "Overcast, diffuse",
    "atmosphere": "Green-industrial, hardworking"
  },
  "composition": {
    "camera_angle": "Mid-shot of machinery",
    "focal_point": "Massive carbon-capture fans"
  },
  "objects": [
    {
      "id": "machinery",
      "visual_attributes": {
        "appearance": "Moss-covered industrial fans",
        "features": "Solar-heating networks"
      }
    }
  ]
}
```

### 8. Redez (Amphibious Logistics)
> *Prompt:* A city on the edge of the world-ocean built for Muskeg terrain. Buildings are built on massive pontoons. Amphibious trucks with oversized tracks moving between floating warehouses over ground too soft for wheels.

```json
{
  "meta": {
    "image_type": "Action/Vehicle Focus",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "City on the ocean edge built for Muskeg terrain.",
    "lighting": "Grey daylight",
    "atmosphere": "Logistical, muddy, heavy"
  },
  "composition": {
    "camera_angle": "Tracking shot of a vehicle",
    "focal_point": "Amphibious truck with oversized tracks"
  },
  "objects": [
    {
      "id": "vehicle",
      "visual_attributes": {
        "appearance": "Truck with oversized tracks",
        "action": "Moving between warehouses"
      }
    },
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Warehouses on pontoons"
      }
    }
  ]
}
```

### 9. Nechars (The Frost Pillar)
> *Prompt:* The northernmost frontier. A high-tech outpost built on deep permafrost. Architecture features heavy insulation and heat-sinking pylons. Permafrost seed vaults and digital archival archives deep underground. Steam discharging into the frozen air.

```json
{
  "meta": {
    "image_type": "Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Northernmost high-tech frontier outpost on deep permafrost.",
    "lighting": "Harsh white ice glare",
    "atmosphere": "Extreme cold, survivalist, secure"
  },
  "composition": {
    "camera_angle": "Wide shot showing isolation",
    "focal_point": "Heat-sinking pylons supporting the base"
  },
  "objects": [
    {
      "id": "outpost",
      "visual_attributes": {
        "appearance": "Heavy insulation, pylons",
        "features": "Steam discharging"
      }
    }
  ]
}
```

---

## 🏛️ Heraldic Assets: Flags and Coats of Arms
**Theme:** Minimalist, Professional Heraldry, Modern-Ancient Synthesis.

### 🚩 National Flags (3:2 Ratio)
> *Prompt Template:* A minimalist national flag for [Country/City]. 3:2 aspect ratio. [Field Color] field. In the center, a [Icon Description] icon with sleek, modern geometric lines. Professional heraldic design, flat vector style.

### 🛡️ Coats of Arms (Heater Shield)
> *Prompt Template:* A coat of arms for [Country/City]. A [Shield Color] heater-shaped shield. In the center, a [Central Charge Description]. [Secondary Element Description if applicable]. Professional heraldic design, clean lines, slightly metallic finish. White background.

### 🏙️ Examples:
1. **Skýjakot (Metropolis):**
   * **Flag:** Violet field with a white stylized cloud icon and a silver pine tree growing through it.
   * **Arms:** Violet shield with a silver pine tree and three small glowing blue sparks.
2. **Yokasy (Golden Isles):**
   * **Flag:** Red sandstone color with a stylized golden sun-disk.
   * **Arms:** Sandstone shield with a golden arch and a single olive branch.
3. **NorKunta Prime (Industrial Center):**
   * **Flag:** Charcoal grey with a glowing cyan horizontal line.
   * **Arms:** Charcoal shield with a massive silver steel gear and a blue ice-crystal.

---

## 🌊 Ax Pelak Yeldo (Central Archipelago)
**Theme:** Maritime High-Tech, Floating Research Hubs, Volcanic-Glass Fusion.

> *Prompt:* A dense cluster of high-tech tropical islands. Sleek white maritime research platforms floating between ancient volcanic peaks. Advanced autonomous hydro-vessels navigating narrow channels. Crystal clear turquoise water and vibrant reefs.

```json
{
  "meta": {
    "image_type": "Aerial Tropical",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Dense cluster of high-tech tropical islands.",
    "lighting": "Bright tropical sun, turquoise water",
    "atmosphere": "Vibrant, clean, advanced"
  },
  "composition": {
    "camera_angle": "Aerial drone shot",
    "focal_point": "White platforms floating between peaks"
  },
  "objects": [
    {
      "id": "platforms",
      "visual_attributes": {
        "appearance": "Sleek white maritime research stations",
        "position": "Floating"
      }
    },
    {
      "id": "vessels",
      "visual_attributes": {
        "appearance": "Autonomous hydro-vessels",
        "action": "Navigating channels"
      }
    }
  ]
}
```

---

## 🏰 Continent 5: Antarmund (Eastern Super-continent)
**Theme:** Neo-Traditionalist, Oceanic Temperate, Alchemical Engineering, North-South Gradient.

### 1. NorKunta (Northern Industrial Powerhouse)
> *Prompt:* High-altitude aerial view of NorKunta Prime, a colossal industrial-residential metropolis spanning a glacial valley. The city center is dominated by massive steel foundries and automotive assembly plants, their smokestacks rising like cathedral spires, lit by the amber glow of molten metal. Surrounding the industrial core are high-density residential districts ('The Hearths')—brutalist concrete mega-blocks built into the valley walls, glowing with warm internal light to combat the arctic night. Commercial avenues cut through the snow like veins of neon fire, bustling with open-air markets and heated transport hubs. The deep-water harbor is packed with massive ice-breaker ships and heavy-lift gantry cranes. Snow falls gently over the gritty, powerful, high-tech landscape.

```json
{
  "meta": {
    "image_type": "Aerial Metropolis",
    "aspect_ratio": "4:3"
  },
  "global_context": {
    "scene_description": "Colossal industrial-residential metropolis in a glacial valley.",
    "lighting": "Amber industrial glow, warm residential lights, neon commercial strips",
    "atmosphere": "Gritty, powerful, bustling, snowy"
  },
  "composition": {
    "camera_angle": "High-altitude aerial looking down the valley",
    "focal_point": "The integration of industry and residential zones"
  },
  "objects": [
    {
      "id": "industry",
      "visual_attributes": {
        "appearance": "Steel foundries like cathedrals",
        "action": "Molten metal glow"
      }
    },
    {
      "id": "residential",
      "visual_attributes": {
        "appearance": "Brutalist concrete mega-blocks",
        "location": "Built into valley walls",
        "lighting": "Warm internal light"
      }
    },
    {
      "id": "commercial",
      "visual_attributes": {
        "appearance": "Neon-lit avenues",
        "features": "Heated transport hubs"
      }
    },
    {
      "id": "harbor",
      "visual_attributes": {
        "appearance": "Deep-water port with ice-breakers"
      }
    }
  ]
}
```

### 2. Jarnhöfn (Iron Harbor)
> *Prompt:* High-altitude aerial shot of Jarnhöfn, a sprawling industrial-residential metropolis on the edge of a frozen sea. In the foreground, colossal naval shipyards swarm with gantry cranes looming over the unfinished hulls of nuclear ice-breakers, the water choked with jagged ice but kept open by thermal discharge. The midground reveals 'The Barracks'—density packed residential districts of blocky reinforced concrete, glowing with warm orange streetlights and dotted with neon-lit commercial zones around heated rail lines. In the background, the frozen ocean stretches to the horizon, broken only by the thermal wakes of departing ships. Atmosphere is heavy, metallic, and bustling with survivalist energy.

```json
{
  "meta": {
    "image_type": "Aerial Cityscape",
    "aspect_ratio": "4:3"
  },
  "global_context": {
    "scene_description": "Sprawling industrial-residential metropolis on a frozen coast.",
    "lighting": "Arctic twilight with warm orange city lights and neon signs",
    "atmosphere": "Bustling, cold, survivalist, heavy"
  },
  "composition": {
    "camera_angle": "High-altitude aerial looking down at the coast",
    "focal_point": "The contrast between the dark shipyard and the glowing hab-blocks"
  },
  "objects": [
    {
      "id": "districts",
      "visual_attributes": {
        "residential": "Dense blocky concrete hab-blocks",
        "commercial": "Neon-lit modular zones near rails",
        "lighting": "Warm orange streetlights"
      }
    },
    {
      "id": "industry",
      "visual_attributes": {
        "appearance": "Nuclear naval shipyards",
        "action": "Cranes constructing ice-breakers"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Frozen sea",
        "features": "Thermal wakes and jagged ice"
      }
    }
  ]
}
```

### 3. Titansmidja (Titan's Forge)
> *Prompt:* High-altitude aerial view of Titansmidja, a concentric industrial city sited inside a massive blackened volcanic caldera surrounded by a blinding white glacier. A small, fast-flowing river of glacial meltwater cuts through the city center, steaming as it runs past geothermal exchanges. The central crater houses the 'Magma Core' heavy industry—robotic assembly lines glowing with molten metal. Radiating outwards are the residential rings: terraced stone-and-steel apartments climbing the caldera walls, illuminated by warm amber streetlights. Commercial districts cluster around the riverbanks, featuring glass-roofed markets and heated plazas. Thick columns of steam rise from the river and the forge, blending with the clouds.

```json
{
  "meta": {
    "image_type": "Cinematic Aerial",
    "aspect_ratio": "4:3"
  },
  "global_context": {
    "scene_description": "Concentric industrial city inside a volcanic caldera with a river.",
    "lighting": "Glow of molten metal and warm city lights against white snow",
    "atmosphere": "Intense, geothermally active, structured"
  },
  "composition": {
    "camera_angle": "High-altitude aerial establishing shot",
    "focal_point": "The river cutting through the glowing industrial core"
  },
  "objects": [
    {
      "id": "landscape",
      "visual_attributes": {
        "appearance": "Black volcanic caldera surrounded by glacier",
        "river": "Fast-flowing steaming meltwater"
      }
    },
    {
      "id": "industry",
      "visual_attributes": {
        "appearance": "Magma Core heavy industry",
        "action": "Glowing with molten metal"
      }
    },
    {
      "id": "residential",
      "visual_attributes": {
        "appearance": "Terraced stone-and-steel apartments",
        "location": "Climbing caldera walls",
        "lighting": "Warm amber"
      }
    },
    {
      "id": "commercial",
      "visual_attributes": {
        "appearance": "Glass-roofed markets",
        "location": "Riverbanks"
      }
    }
  ]
}
```

### 4. Aero-Valli (Aero Rampart)
> *Prompt:* High-altitude aerial shot of Aero-Valli, a sprawling and highly active military airbase carved into a jagged mountain ridge. The facility features a main runway paralleled by taxiways and fortified blast pens. Behind the flight line lies a dense cantonment area: rows of austere multi-story concrete barracks for personnel, reinforced command bunkers, and modular housing blocks for civilian contractors. A central administrative complex and communications relay dominates the ridge. The tarmac is busy with ground operations: maintenance crews swarming around experimental fighter jets, fuel trucks refueling aircraft, and loaders arming hardpoints. The architecture is utilitarian, brutalist, and reinforced against the elements. The sense of scale and operational tempo is immense.

```json
{
  "meta": {
    "image_type": "Realistic Military Airbase",
    "aspect_ratio": "4:3"
  },
  "global_context": {
    "scene_description": "Busy high-altitude military airbase with extensive housing and support.",
    "lighting": "Clear, harsh high-altitude sunlight casting sharp shadows",
    "atmosphere": "Active, disciplined, high-tech military operations"
  },
  "composition": {
    "camera_angle": "High-altitude aerial survey",
    "focal_point": "The busy apron and taxiways"
  },
  "objects": [
    {
      "id": "infrastructure",
      "visual_attributes": {
        "appearance": "Main runway with parallel taxiways",
        "features": "Blast pens, reinforced hangars, radar arrays"
      }
    },
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Grid of concrete barracks and bunkers",
        "secondary": "Modular civilian housing blocks",
        "feature": "Central administrative complex"
      }
    },
    {
      "id": "aircraft_active",
      "visual_attributes": {
        "appearance": "Experimental fighter jets",
        "action": "Taxiing, refueling, arming",
        "count": "Multiple units in motion"
      }
    },
    {
      "id": "ground_support",
      "visual_attributes": {
        "appearance": "Fuel trucks and loaders",
        "personnel": "Maintenance crews on tarmac"
      }
    }
  ]
}
```

### 5. Sydgard (The Green Gateway)
> *Prompt:* High-altitude aerial view of Sydgard, a sprawling temperate metropolis situated in a massive gulf where five major rivers converge into the sea. The city center features dense clusters of glass-and-steel high-rises along the waterfronts, surrounded by extensive green recreational parks and busting commercial districts. Radiating outward are vast, leafy suburbs of single-family homes that stretch along the riverbanks and into the rolling hills. The five rivers cut through the city like arteries, spanned by sleek modern bridges. The deep blue gulf is busy with maritime traffic, while the city layout integrates nature with urban sprawl.

```json
{
  "meta": {
    "image_type": "Modern Eco-City Aerial",
    "aspect_ratio": "4:3"
  },
  "global_context": {
    "scene_description": "Sprawling metropolis at the convergence of five rivers.",
    "lighting": "Bright daylight, clear visibility",
    "atmosphere": "Vibrant, expansive, connected"
  },
  "composition": {
    "camera_angle": "High-altitude aerial looking inland from the gulf",
    "focal_point": "The convergence of the rivers at the city center"
  },
  "objects": [
    {
      "id": "geography",
      "visual_attributes": {
        "features": "Massive gulf, five converging rivers",
        "surroundings": "Rolling green hills"
      }
    },
    {
      "id": "urban_core",
      "visual_attributes": {
        "appearance": "Glass-and-steel high-rises",
        "location": "Waterfronts and city center",
        "features": "Commercial districts, recreational parks"
      }
    },
    {
      "id": "suburbs",
      "visual_attributes": {
        "appearance": "Sprawl of single-family homes",
        "location": "Radiating outwards along riverbanks",
        "vibe": "Leafy, residential"
      }
    }
  ]
}
```

### 6. Cryo-Vault 09 (The Seed Bank)
> *Prompt:* Cinematic shot of Cryo-Vault 09, a heavily fortress-like entrance set into a permafrost cliff. Massive blast doors are guarded by automated turrets and patrolling drones. Scientists in orange extreme-cold gear are unloading canisters from a heavy snow-crawler. The structure is brutalist concrete reinforced with steel, covered in frost.

```json
{
  "meta": {
    "image_type": "Sci-Fi Bunker",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Heavily guarded seed bank entrance in permafrost.",
    "lighting": "Overcast, flat arctic light",
    "atmosphere": "Secure, sterile, important"
  },
  "composition": {
    "camera_angle": "Eye-level establishing shot",
    "focal_point": "The massive blast doors"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Brutalist concrete bunker",
        "features": "Blast doors, automated turrets"
      }
    },
    {
      "id": "characters",
      "visual_attributes": {
        "appearance": "Scientists in orange gear",
        "action": "Unloading cargo"
      }
    }
  ]
}
```

### 7. Borealis Station (Aurora Harvest)
> *Prompt:* A night shot of Borealis Station on the open tundra. The facility is dominated by massive "Aurora Harvesting" arrays—tall, spiral coils that glow in sympathy with the vibrant green and purple northern lights overhead. The station itself is a cluster of dome habitats connected by heated tunnels. The snow reflects the dazzling light show from the sky and the machines.

```json
{
  "meta": {
    "image_type": "Sci-Fi Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Research station harvesting aurora energy.",
    "lighting": "Night time, vibrant green/purple aurora glow",
    "atmosphere": "Wonder, scientific, electrical"
  },
  "composition": {
    "camera_angle": "Low angle looking up at coils and aurora",
    "focal_point": "The connection between the coils and the sky"
  },
  "objects": [
    {
      "id": "machinery",
      "visual_attributes": {
        "appearance": "Spiral energy coils",
        "action": "Glowing with aurora energy"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Snowy tundra",
        "sky": "Vibrant northern lights"
      }
    }
  ]
}
```

### 8. Koldfisk Rig (Aquaculture Hub)
> *Prompt:* Wide aerial shot of Koldfisk Rig, a massive industrial platform centered on a frozen lake. Large circular bio-domes melt through the ice, revealing dark water teeming with bio-engineered fish. Teal underwater lights illuminate the depths. Steam rises from the heated domes against the snowy landscape. Industrial walkways connect the domes to a central processing plant.

```json
{
  "meta": {
    "image_type": "Industrial Aerial",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Inland aquaculture facility on frozen lake.",
    "lighting": "Grey daylight with teal underwater glow",
    "atmosphere": "Industrial, aquatic, cold"
  },
  "composition": {
    "camera_angle": "High angle aerial",
    "focal_point": "The glowing bio-domes"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Circular bio-domes",
        "feature": "Heated, melting the ice"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Frozen lake surface"
      }
    }
  ]
}
```

### 9. Ice-Hauler's Rest (Truck Stop)
> *Prompt:* A gritty, atmospheric ground-level shot of a massive truck stop on the ice road. Rugged, armored 18-wheeler "Ice Haulers" with spiked tires are parked in rows, their engines idling and emitting steam. A central hub building glows with neon "OPEN" and "DINER" signs, cutting through the swirling snow. Weather-beaten drivers walk between vehicles.

```json
{
  "meta": {
    "image_type": "Atmospheric Slice-of-Life",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Gritty truck stop on the ice road.",
    "lighting": "Headlights, neon signs, swirling snow",
    "atmosphere": "Gritty, tired, warm refuge"
  },
  "composition": {
    "camera_angle": "Eye-level from the parking lot",
    "focal_point": "A massive armored truck in foreground"
  },
  "objects": [
    {
      "id": "vehicles",
      "visual_attributes": {
        "appearance": "Armored ice-hauler trucks",
        "details": "Spiked tires, dirty snow"
      }
    },
    {
      "id": "building",
      "visual_attributes": {
        "appearance": "Hub with neon signs",
        "atmosphere": "Warm inviting glow"
      }
    }
  ]
}
```

### 10. Glacial Edge (Expedition Camp)
> *Prompt:* A vibrant, colorful forward operating base at the foot of a colossal blue glacier wall. Bright orange and yellow modular habitats and dome tents stand out against the white snow. Expedition rovers are being loaded with climbing gear. The glacier wall looms hundreds of meters high in the background, signaling the start of the 'High Ice'.

```json
{
  "meta": {
    "image_type": "Adventure Photography",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Expedition base at the foot of a glacier.",
    "lighting": "Bright, high-contrast sunlight",
    "atmosphere": "Adventure, preparation, scale"
  },
  "composition": {
    "camera_angle": "Wide shot showing scale of glacier",
    "focal_point": "Contrast between small colorful tents and huge ice wall"
  },
  "objects": [
    {
      "id": "camp",
      "visual_attributes": {
        "appearance": "Colorful tents and habs",
        "colors": "Orange, Yellow"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Colossal blue glacier wall"
      }
    }
  ]
}
```

### 11. Echo Ridge (Mining Outpost)
> *Prompt:* A precarious mining outpost clinging to a jagged, wind-swept mountain ridge. Scaffolding and drilling rigs hang over the edge. Large rock-crushers pulverize stone, creating dust clouds that mix with the snow. Industrial floodlights cut through the dust. The architecture is temporary, industrial, and bolted directly into the rock.

```json
{
  "meta": {
    "image_type": "Industrial Concept",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Mining outpost on a jagged ridge.",
    "lighting": "Industrial floodlights in dust/snow",
    "atmosphere": "Dangerous, noisy, industrial"
  },
  "composition": {
    "camera_angle": "Side profile of the ridge",
    "focal_point": "Drilling rigs hanging over the edge"
  },
  "objects": [
    {
      "id": "machinery",
      "visual_attributes": {
        "appearance": "Drills and rock crushers",
        "location": "Clinging to cliff"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Jagged mountain ridge",
        "weather": "Wind-swept"
      }
    }
  ]
}
```

### 12. Sleet-Watch (Weather Outpost)
> *Prompt:* A remote hamlet dominated by white spherical radomes and sensor masts. Located on a rocky coastal promontory where dark storm waves crash against the cliffs. The buildings are hunkered low, aerodynamic to survive the constant gale-force winds. Rain and sleet lash the lens.

```json
{
  "meta": {
    "image_type": "Moody Landscape",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Weather monitoring station in a storm.",
    "lighting": "Dark, moody, grey",
    "atmosphere": "Stormy, isolated, technical"
  },
  "composition": {
    "camera_angle": "Wide shot of the promontory",
    "focal_point": "White radomes against dark sky"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Radomes and sensor masts",
        "style": "Aerodynamic low bunkers"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Stormy coast",
        "action": "Waves crashing"
      }
    }
  ]
}
```

### 13. Thermal-Springs (Spa Town)
> *Prompt:* A cozy, inviting village centering on large natural hot spring pools. Steam rises from the turquoise water, contrasting with the surrounding snow-covered pine trees. Traditional timber-frame lodges with warm yellow windows ring the pools. People are relaxing in the water despite the freezing air.

```json
{
  "meta": {
    "image_type": "Travel/Leisure",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Hot spring spa town in winter.",
    "lighting": "Soft twilight, steam, warm windows",
    "atmosphere": "Relaxing, cozy, thermal"
  },
  "composition": {
    "camera_angle": "Eye-level across the pool",
    "focal_point": "Steam rising from turquoise water"
  },
  "objects": [
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Natural hot springs",
        "feature": "Steam and turquoise water"
      }
    },
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Timber-frame lodges",
        "lighting": "Warm yellow"
      }
    }
  ]
}
```

### 5. Guldhorn (Finance Hub)
> *Prompt:* Gold-glass skyscrapers that resemble giant gothic cathedrals. Precision-engineered bridges with digital heraldic flags. Dense temperate rainforest bordering the financial core. Ultra-luxurious.

```json
{
  "meta": {
    "image_type": "Architectural Visualization",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Gold-glass skyscrapers resembling giant gothic cathedrals.",
    "lighting": "Golden hour, reflective",
    "atmosphere": "Luxurious, imposing, wealthy"
  },
  "composition": {
    "camera_angle": "Low angle looking up skyscrapers",
    "focal_point": "Gothic details on glass towers"
  },
  "objects": [
    {
      "id": "skyscrapers",
      "visual_attributes": {
        "appearance": "Gold-glass, neo-gothic shape",
        "style": "Cathedral-like"
      }
    },
    {
      "id": "bridges",
      "visual_attributes": {
        "features": "Digital heraldic flags"
      }
    }
  ]
}
```

### 3. Norgborg (The Shield)
> *Prompt:* A militaristic coastal smart-city in the Southern Rim. Massive automated naval batteries and sleek patrol warships in the harbor. Architecture is angular and gray, featuring graphene-reinforced walls. Cool, misty temperate climate.

```json
{
  "meta": {
    "image_type": "Military Sci-Fi",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Militaristic coastal smart-city with naval batteries.",
    "lighting": "Cool, grey, misty",
    "atmosphere": "Secure, disciplined, strong"
  },
  "composition": {
    "camera_angle": "Overlooking the harbor defenses",
    "focal_point": "Sleek patrol warships"
  },
  "objects": [
    {
      "id": "defenses",
      "visual_attributes": {
        "appearance": "Massive automated naval batteries",
        "material": "Graphene-reinforced walls"
      }
    },
    {
      "id": "ships",
      "visual_attributes": {
        "appearance": "Sleek angular warships"
      }
    }
  ]
}
```

### 4. Valermond (City of Light)
> *Prompt:* Coastal city dedicated to high physics, located in a deciduous forest. Sleek glass spires pulsing with clean white light. Famous for seasonal changes—blazing red/orange autumn leaves around the physics labs. Sunset lighting.

```json
{
  "meta": {
    "image_type": "Vibrant Architectural",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Coastal city in a deciduous forest with glass spires.",
    "lighting": "Sunset lighting, clean white pulse from spires",
    "atmosphere": "Academic, brilliant, autumnal"
  },
  "composition": {
    "camera_angle": "Wide shot of the skyline",
    "focal_point": "Glass spires amidst red/orange autumn leaves"
  },
  "objects": [
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Sleek glass spires",
        "action": "Pulsing with white light"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Deciduous forest in autumn colors"
      }
    }
  ]
}
```

### 5. Metsemania (Nanotech Timber)
> *Prompt:* A city built within a temperate rainforest. Architecture merges with massive Old-Growth Redwood and Sequoia trees. Buildings use nanotechnology-enhanced cellulose structures. GLEAMING laboratory towers merging with giant ancient bark.

```json
{
  "meta": {
    "image_type": "Bio-Futurism",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "City built within a temperate rainforest merging with trees.",
    "lighting": "Dappled forest light, gleaming labs",
    "atmosphere": "Organic, ancient, scientific"
  },
  "composition": {
    "camera_angle": "Looking up a giant tree",
    "focal_point": "Lab tower merging with bark"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Gleaming laboratory towers",
        "action": "Merging with Old-Growth Sequoias"
      }
    },
    {
      "id": "material",
      "visual_attributes": {
        "type": "Nanotech-enhanced cellulose"
      }
    }
  ]
}
```

### 6. Laendamania (Global Media)
> *Prompt:* A hyper-vibrant neon city in the Temperate Rim. Massive holographic displays broadcasting across vertical urban canyons. Glass towers with digital "skins". Lush green hills in the distance.

```json
{
  "meta": {
    "image_type": "Cyberpunk/Neon",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Hyper-vibrant neon city in vertical canyons.",
    "lighting": "Multi-colored holographic glow",
    "atmosphere": "Loud, media-centric, energetic"
  },
  "composition": {
    "camera_angle": "Down a vertical urban canyon",
    "focal_point": "Massive holographic displays"
  },
  "objects": [
    {
      "id": "buildings",
      "visual_attributes": {
        "appearance": "Glass towers with digital skins",
        "features": "Holographic broadcasts"
      }
    }
  ]
}
```

### 7. Melynmania (Traditional-Digital Arts)
> *Prompt:* A picturesque riverside city in the southern temperate zone. Blending classical stone architecture with advanced holographic projection mapping. Artisans using digital chisels on stone.

```json
{
  "meta": {
    "image_type": "Artistic Concept",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Picturesque riverside city blending stone and holograms.",
    "lighting": "Soft natural light + digital projection",
    "atmosphere": "Cultural, artistic, peaceful"
  },
  "composition": {
    "camera_angle": "Mid-shot of an artisan",
    "focal_point": "Artisan using digital chisel on stone"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Classical stone",
        "features": "Holographic projection mapping"
      }
    }
  ]
}
```

### 8. Sigmarignen (The Eternal Capital)
> *Prompt:* An ancient city retrofitted with holographic art installations. Traditional architecture with solar-panel roofs. Surrounded by rolling temperate forests and historical monuments.

```json
{
  "meta": {
    "image_type": "Historical/Modern Mix",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Ancient retrofitted city surrounded by forest.",
    "lighting": "Daylight",
    "atmosphere": "Regal, timeless, adaptive"
  },
  "composition": {
    "camera_angle": "Wide establishing shot",
    "focal_point": "Traditional building with solar-panel roof"
  },
  "objects": [
    {
      "id": "building",
      "visual_attributes": {
        "style": "Traditional/Historical",
        "features": "Solar-panel roofs, holographic art"
      }
    }
  ]
}
```

### 9. Nargkes (High-Pressure Industry)
> *Prompt:* Heavy industrial city focused on deep-sea and geothermal engineering. Massive steam-rams and glowing red piping running between modern industrial towers.

```json
{
  "meta": {
    "image_type": "Industrial Steampunk/Modern",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Heavy industrial city with seam-rams and piping.",
    "lighting": "Red glow from pipes, steam",
    "atmosphere": "Heavy, pressurized, intense"
  },
  "composition": {
    "camera_angle": "Low angle industrial",
    "focal_point": "Massive steam-rams"
  },
  "objects": [
    {
      "id": "machinery",
      "visual_attributes": {
        "appearance": "Glowing red piping",
        "action": "Steam-rams operating"
      }
    }
  ]
}
```

### 10. Norginde (Precision Tools)
> *Prompt:* A clean, clinical city focused on micro-engineering. Buildings look like polished internal components of a watch. Minimalist white-and-silver aesthetic.

```json
{
  "meta": {
    "image_type": "Minimalist High-Tech",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Clean, clinical city focused on micro-engineering.",
    "lighting": "Bright white laboratory light",
    "atmosphere": "Precise, sterile, perfect"
  },
  "composition": {
    "camera_angle": "Symmetrical architectural shot",
    "focal_point": "Polished watch-component-like buildings"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Silver and white",
        "style": "Watch-component aesthetic"
      }
    }
  ]
}
```

### 11. Kasim'Merik (Sea Gate)
> *Prompt:* A massive bridge-city spanning a strait. Architecture features aerodynamic wind-breaking structures and integrated maritime power turbines.

```json
{
  "meta": {
    "image_type": "Architectural Wide",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Massive bridge-city spanning a strait.",
    "lighting": "Windy, bright daylight",
    "atmosphere": "Functional, aerodynamic, connective"
  },
  "composition": {
    "camera_angle": "Aerial side-profile",
    "focal_point": "The bridge span"
  },
  "objects": [
    {
      "id": "structure",
      "visual_attributes": {
        "appearance": "Aerodynamic wind-breaking bridge",
        "features": "Integrated maritime turbines"
      }
    }
  ]
}
```

### 12. Dirka'Merik (Logistics Core)
> *Prompt:* A city of automated warehouses and high-speed freight rails. Modular architecture that can be rearranged by massive rail-mounted cranes.

```json
{
  "meta": {
    "image_type": "Industrial Logistics",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "City of automated warehouses and freight rails.",
    "lighting": "Functional floodlights",
    "atmosphere": "Busy, automated, efficient"
  },
  "composition": {
    "camera_angle": "High angle overlooking rail yard",
    "focal_point": "Massive rail-mounted cranes"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "Modular containers/warehouses",
        "action": "Being rearranged by cranes"
      }
    }
  ]
}
```

### 13. Fyny'Dor (The Breadbasket)
> *Prompt:* A vast agricultural paradise in the temperate grasslands. The only significant flat, green space for large-scale grain farming. Vertical hydro-farming towers and massive automated harvesters.

```json
{
  "meta": {
    "image_type": "Agricultural Sci-Fi",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Vast agricultural paradise in temperate grasslands.",
    "lighting": "Golden hour over wheat fields",
    "atmosphere": "Abundant, peaceful, expansive"
  },
  "composition": {
    "camera_angle": "Wide horizon shot",
    "focal_point": "Vertical hydro-farming towers"
  },
  "objects": [
    {
      "id": "structures",
      "visual_attributes": {
        "appearance": "Vertical hydro-farming towers"
      }
    },
    {
      "id": "machinery",
      "visual_attributes": {
        "appearance": "Massive automated harvesters"
      }
    }
  ]
}
```

### 14. Meit'Val (The Southern Retreat)
> *Prompt:* A luxury coastal resort state in the deep temperate south. Architecture features floating glass villas and sub-aquatic hotels. Golden beaches and purple sunsets.

```json
{
  "meta": {
    "image_type": "Luxury Travel Photography",
    "aspect_ratio": "16:9"
  },
  "global_context": {
    "scene_description": "Luxury coastal resort with floating villas.",
    "lighting": "Purple sunset",
    "atmosphere": "Relaxing, expensive, beautiful"
  },
  "composition": {
    "camera_angle": "Water level shot",
    "focal_point": "Floating glass villas"
  },
  "objects": [
    {
      "id": "architecture",
      "visual_attributes": {
        "appearance": "floating glass villas",
        "features": "Sub-aquatic levels"
      }
    },
    {
      "id": "environment",
      "visual_attributes": {
        "appearance": "Golden beaches",
        "lighting": "Purple sunset"
      }
    }
  ]
}
```

## ??? Heraldry Prompts
See [heraldry_prompts.md](file:///g:/Mi%20unidad/01_Alex/30_Tecnologia_y_Proyectos/World_Building_Project/03_Applications/Map_Viewer/heraldry_prompts.md) for a complete list of 110+ heraldry image generation prompts for all countries and cities.
