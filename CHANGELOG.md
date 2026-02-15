# Changelog

## [3.1.0] - 2026-02-15
### 🏗️ Global Hierarchy Refactor & Map Fix
*   **Data Hierarchy Flattening:** Removed all intermediate regional groupings (e.g., "Southern Prosperity Rim", "The Dark-Water States", "The Golden Isles") and promoted all constituent states to top-level **Country** objects within their respective continents. The world now has a clean 3-tier hierarchy: **Continent → Country → City**.
*   **Betereko Consolidation:** Merged "The Plateau" and "Betereko" into a single unified **Continent-State** (similar to Australia). **Apex** is the sole capital.
*   **Map Display Crash Fix:** Identified and resolved a critical bug where an invalid city type (`industrial` for Pelak) was crashing the Map Viewer's marker loading loop, preventing all Mirelands and Antarmund cities from rendering. Added a defensive fallback in `js/app.js` for unknown city types.
*   **Wiki Regeneration:** Rebuilt the multi-page HTML Encyclopedia to reflect the new 36-country, 61-city hierarchy.
*   **Data Integrity:** Validated all 61 city entries for unique IDs, valid coordinates, standardized types, and correct color codes.

## [3.0.0] - 2026-02-14
### 🖼️ Image Carousel & Sidebar Polish
*   **Sidebar Image Carousel:** Replaced the static hero image in the Map Viewer sidebar with a fully interactive **multi-image carousel**. Users can now browse all generated landscapes for a city using navigation arrows and dot indicators.
*   **Wiki Image Carousel:** Updated `generate_wiki.py` to detect multiple city images and embed CSS-based carousels into each wiki city profile infobox.
*   **City Images API:** Added a new `/api/city-images` endpoint to `server.js` that scans the `assets/images/` directory to dynamically return all available images for a given city.
*   **Sidebar Display Fix:** Fixed a critical CSS flex-layout bug where the carousel container was collapsed to 0px height by the parent `display: flex`. Resolved with `flex-shrink: 0` and `min-height`.
*   **Binary Serving Fix:** Corrected binary image serving in `server.js` (removed erroneous `utf-8` encoding for non-text files).
*   **Cache-Busting Headers:** Added `Cache-Control: no-cache` headers to the development server to prevent stale CSS/JS/HTML during active development.
*   **Climate Legend:** Added a toggle-able Leaflet legend control for the Climate layer, populated from `colorToClimate` data.

## [2.9.0] - 2026-02-14
### 🎨 Visual & Interactive Polish
*   **Wiki Dark Mode:** Implemented a default slate-dark theme for the encyclopedia, improving readability and matching the project's modern aesthetic.
*   **Wiki Lightbox:** Added a full-screen image preview modal for all flags, coats of arms, and reference landscapes within the wiki.
*   **Asset Hybridization:** Developed a cost-effective separate pipeline for Heraldry (Flash model) vs Landscapes (Pro model).
*   **Sidebar Integration:** Added direct "Wiki" concept links to the interactive map sidebar for seamless navigation between the map and lore.

## [2.8.0] - 2026-02-11
### 📚 Kaelia Encyclopedia & Heraldry
*   **Wiki Expansion:** Transformed the single-page wiki into a comprehensive **Multi-Page Encyclopedia** (`wiki/index.html`) with dedicated profiles for all 5 continents, 40 countries, and 74 cities.
*   **Heraldry Integration:** Completed the **Global Heraldry System**. Every entity now possesses a unique, lore-accurate **Motto** and **Visual Description** (Flag/Coat of Arms) in the master data.
*   **Map Viewer:** Added a **"Wiki" Floating Action Button (FAB)** for direct access to the encyclopedia.
*   **Data Integrity:** Validated 375+ internal wiki links and ensured 100% city coverage for all nations.
*   **Tools:** Created `verify_wiki_links.py` for automated crawler testing and `heraldry_prompts.md` for batch asset generation.

## [2.7.0] - 2026-02-08
### 🗺️ Data Enrichment & Heraldry System
*   **Altitude Integration:** Implemented high-fidelity altitude mapping using 16-bit MDR terrain data. Cities now display precise elevation in meters.
*   **Heraldry System:** Integrated a global heraldry system. Added mottos, visual descriptions, and asset placeholders (Flags/Coats of Arms) for all 9 countries and 43 cities.
*   **Sidebar Refinement:** Completely reordered and restyled the Sidebar Details View. Added descriptive icons (📍, 🌦️, 🏔️, 👥, 🏳️) and standardized data presentation.
*   **Automation:** Developed `batch_heraldry.py` and `update_altitudes_mdr.py` for large-scale data synchronization and 16-bit to 8-bit map conversion.

## [2.6.0] - 2026-02-08
### ❄️ NorKunta Expansion & UI Polish
*   **New Locations:** Added **Cryo-Vault 09** (Subterranean deep-storage) and **Ice-Hauler's Rest** (Logistics hub).
*   **Lore Updates:** Expanded **Borealis Station** to a 60k population research metropolis and **Koldfisk Rig** to an 80k temperate agricultural hub.
*   **Visual Refinement:** Standardized new aerial/landscape prompts to **4:3 aspect ratio** with enhanced atmospheric details (Dusk, Aurora, Coastal).
*   **UI Tweaks:** Widened Sidebar to 450px and Search Bar to 400px for better readability.

## [2.5.0] - 2026-02-07
### 🚀 Map Viewer 2.0 (Google Maps Refactor)
*   **UI Overhaul:** Complete redesign mimicking Google Maps with a floating search bar, slide-out details drawer, and floating action buttons (FABs).
*   **Search**: Implemented real-time city search with auto-complete and "fly-to" functionality.
*   **Zoom Logic:** City labels now dynamically appear/disappear based on zoom level (Metropolises always visible, Villages only at high zoom).
*   **Code Structure:** Refactored Monolithic `index.html` into modular `css/style.css` and `js/app.js`.
*   **Manual Workflow:** Verified and automated the `02_Visual_Assets` directory structure for upcoming image generation.

## [2.4.0] - 2026-02-05
### 🗺️ Map Viewer Enhanced
*   **Frontier Extraction:** Implemented advanced "Image Difference" algorithm to extract country borders and names from the original map.
*   **Solid-Gold Refinement:** Replaced extracted pixel colors with synthesized "Solid Gold" (RGB 0, 215, 255) to eliminate blue compression artifacts and ensure perfect vector-like clarity.
*   **Coordinate Grid:** Can now toggle a 100x100 global coordinate grid overlay.
*   **Scale Control:** Added dynamic Google-Maps style scale bar (calibrated to Earth-Scale 40,000km).
*   **UI Polish:** Simplified layer menu and established a "Composite" Political view (Satellite + Gold Frontiers) as the default.

## [2.3.0] - 2026-02-04
### 🌍 Unified Biome-Corrected Edition
*   **Climatology:** Synchronized all continental data with Global Biome Scans (Whittaker Classification).
*   **Nordica:** Reclassified as Sub-Arctic/Taiga; updated Gryning, Oighear, and Keunmor lore to fit frozen reality.
*   **Kasy Federation:** Reclassified as Mediterranean/Chaparral; updated Solar-Sea and architectural lore.
*   **Mirelands:** Reclassified as Cold Taiga/Sub-Arctic Swamp; updated Dark-Water States adaptation lore.
*   **Antarmund:** Implemented North-South gradient (Tundra to Temperate Rainforest); reclassified Southern Rim as Oceanic Temperate.
*   **Economy:** Added "Strategic Resource Correction" based on global biome scarcity.

## [2.2.0] - 2026-02-03
### 🗺️ Global Grid Expansion
*   **Geopolitics:** Completed the definitive mapping of all 37 regions and states across five continents and the central archipelago.
*   **Visual Roadmap:** Established a 1:1 directory structure in `02_Visual_Assets/2.0_Regional_Scale/` for every mapped entity.
*   **Prompt Library:** Finalized high-fidelity "Modern-Ancient Synthesis" image generation prompts for all 37 regions.
*   **Archipelago:** Formally integrated `Ax Pelak Yeldo` into the core planetary lore.

## [2.1.0] - 2026-02-03
### 🏗️ Reorganization & Synthesis
*   **Tech Pivot:** Definitive shift to "Modern-Ancient Synthesis" (Information Age world with ancestral roots).
*   **Structure:** Implemented new 4-tier hierarchy (Design Sources, Visual Assets, Applications, Archive).
*   **Public Release:** Extracted project from private parent repo to standalone public GitHub repository.
*   **Licensing:** Officially protected under **CC BY-NC-SA 4.0**.
*   **Standardization:** Renamed all legacy `Planeta 1` files and folders to `Kaelia`.
*   **Prompts:** Expanded AI visualization library with detailed Gryning settlement guides.

## [2.0.0] - 2026-02-02
### 🚀 Rebirth & Restructuring
*   **Renaming:** Project renamed from `Proiectul de lume` to `World_Building_Project`.
*   **Scope Refinement:** Abandoned "Solar System" ambition to focus exclusively on the single, detailed world (Planeta 1).
*   **Conti-Lore:** Expanded `WIKI.md` with detailed descriptions for "The Kasy Federation", "Betereko", "The Mirelands", and "Guldhorn Reaches".
*   **Organization:** Promoted all sub-assets (Videos, Docs) to the project root.
*   **Legacy:** Archived `Sistem solar.xlsx` to `Archive/`.
*   **Documentation:** Created extensive WIKI, ROADMAP, and README in English.

## [1.0.0] - 2014 (approx)
### 🐣 Genesis
*   **Initial Creation:** Project started using Cinema 4D and Fractal Terrains.
*   **Rendering:** Generated high-resolution 3D spins and equirectangular maps.
*   **Lore:** Wrote initial draft of `Continents and countries` (GDoc).
*   **Video:** Produced `Planeta 1 3D full.mov`.
