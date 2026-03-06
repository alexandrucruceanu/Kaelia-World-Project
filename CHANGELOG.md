# Changelog
 
## [3.8.0] - 2026-03-06
### 🤖 Gemini Model Upgrade
*   **Model Migration:** Upgraded all AI generation scripts to the latest recommended models: `gemini-3-flash-preview` (JSON/text) and `gemini-3-pro-image-preview` (vision/image generation).
*   **`complete_world_data.py`:** Migrated from `gemini-2.0-flash` to `gemini-3-flash-preview` for lore and visual schema generation.
*   **`generate_prompts_llm.py`:** Fixed stale description referencing "Gemini 2.0 Flash"; model was already updated.
*   **`generate_assets_hybrid.py`:** Verified correct routing — `MODEL_FAST` targets `gemini-3-flash-preview` for structural/JSON endpoints, `MODEL_PRO` targets `gemini-3-pro-image-preview` for visual generation.
*   **Validation:** All 5 asset types (landscape_main, landscape_seq1, landscape_seq2, heraldry_flag, heraldry_arms) tested with construct-only mode — valid JSON output confirmed.
*   **Documentation:** Updated `README.md`, `ROADMAP.md`, `LLM_PRIMER_PROMPT.md`, and `CHANGELOG.md` to reflect the new models.

## [3.7.0] - 2026-02-21
### 🔐 Security & AI Verification
*   **Git Security:** Added `.env` to the root `.gitignore` to prevent accidental exposure of API keys and credentials.
*   **Gemini Setup Verification:** Audited and verified the `GEMINI_SETUP.md` requirements. Confirmed successful integration of `google-generativeai` and `python-dotenv` for backend services.
*   **Prompt Explorer Launch:** Successfully deployed and verified the dedicated Prompt Explorer tool for real-time AI generation and city data management.
 
## [3.6.0] - 2026-02-19
### 📄 Documentation & Data Schema Optimization
*   **Visual Data Flattening:** Simplified the `visual_data` field in `master_world_data.json` from a complex JSON schema to a plain-text prompt string. Updated the Map Viewer and Prompt Explorer to render and edit this data more efficiently.
*   **Wiki Breadcrumbs:** Enhanced the Kaelia Encyclopedia with a full breadcrumb trail: **Kaelia > Continent > Country > City**, improving navigation and spatial context across all wiki pages.
*   **Wiki Sync Stability:** Improved `sync_wiki.py` with more robust path handling and localized update logic, resolving potential "File not found" errors during synchronization.
*   **Documentation Audit:** Updated `README.md` and `ROADMAP.md` to reflect the latest project state and completed the final infrastructure milestones of Phase 3.

## [3.5.0] - 2026-02-17
### 🔗 Navigation Integration & UI Cleanup
*   **Edit → Prompt Explorer:** The "Edit" button in the Map Viewer sidebar now opens the Prompt Explorer in a new tab, deep-linking directly to the selected city via `?cityId=`. The Prompt Explorer auto-filters and scrolls to the target city with a highlight effect.
*   **Add → Prompt Explorer:** The "Add Location" (➕) FAB in the Map Viewer now opens the Prompt Explorer with an "Add New City" modal (`?mode=add`). The modal features cascading Continent/Country dropdowns and placeholder-guided fields for all city data.
*   **UI Cleanup:** Removed legacy "Generate Visual" buttons and modal from the Map Viewer and "Generate Assets" buttons from the Wiki. Regenerated all wiki pages.
*   **Server Fix:** Fixed `server.js` route matching for `/prompt-explorer` to correctly handle URL query parameters.

## [3.4.0] - 2026-02-17
### 🤖 Prompt Explorer & Wiki Sync Fix
*   **Wiki Synchronization Fix:** Resolved a critical path resolution bug in `sync_wiki.py` that prevented HTML updates. Restored the missing city **"Kaldakinn"** to Oighear and forced a global HTML update.
*   **Prompt Explorer Enhancements:** Added **Continent & Country Filters** with cascading logic to the Prompt Explorer, making it easier to navigate the growing dataset.
*   **City Editing:** Implemented a direct **Edit Mode** for cities. Users can now modify population, descriptions, and JSON fields (Lore, Visual Data) directly from the UI, with changes persisting to `master_world_data.json`.
*   **Prompt Generation Service:** Integrated **Gemini 2.0 Flash** for on-demand prompt generation. Added a "✨ Generate Prompts" button to city cards that creates 5 unique prompt types (Aerial, Street, Reportage, Flag, Arms) and saves them to the prompt explorer.

## [3.3.0] - 2026-02-15
### 🏷️ Movable Labels & Prompt Explorer
*   **Movable Labels:** Enabled **drag-and-drop** functionality for Continent and Country labels in the Map Viewer. Users can now toggle "Move Mode" (Hand FAB) to reposition labels, with new coordinates automatically persisted to `master_world_data.json` via new `PUT` API endpoints.
*   **Prompt Explorer:** Launched a dedicated `/prompt-explorer` tool. A searchable interface to view all 5 prompt types (Landscape Main, Seq1, Seq2, Flag, Arms) for every city, alongside detailed metadata (Type, Biome, Lore) and a **Similarity Score** metric to gauge prompt accuracy.
*   **Prompt Migration:** Migrated all hardcoded prompt generation logic to a persistent JSON-based system.
*   **Visual Enhancements:** Fixed the "Aerial" camera angle in `landscape_main` prompts to be "High-angle oblique" (45-degree) for better artistic composition.

## [3.2.0] - 2026-02-15
### 🌐 3D Globe View & Generation API
*   **3D Globe View:** Integrated `globe.gl` library to render an interactive 3D globe. City markers are projected onto the sphere with color-coded points, hover labels, and click-through to the existing sidebar details. Auto-rotate and a **2D/3D Toggle FAB** (🌍/🗺️) allow seamless switching between the flat map and the globe.
*   **Generation API Expansion:** Expanded `server.js` with two new endpoints: `/api/construct-prompt` (returns AI-ready prompts from world data) and `/api/generate-visual` (triggers Python-based image generation with type-aware routing for landscapes and heraldry). Includes automatic **file management** (sequential naming, archiving old heraldry to `_archive/`).
*   **Heraldry Prompt Constructor:** Added `construct_heraldry_prompt()` to `generate_assets_hybrid.py` for data-driven, lore-aware flag and coat of arms prompt generation.
*   **Asset Auditor:** Created `check_assets.js` to validate all city image references in `master_world_data.json` against the actual filesystem, producing a detailed `asset_report_utf8.txt`.
*   **Wiki Regeneration:** Regenerated all 61 city, 36 country, and 5 continent wiki pages to reflect the latest data hierarchy and carousel support.
*   **App Restructure:** Reorganized the full Map Viewer application (assets, scripts, wiki content) into the public repository for self-contained deployment.

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
