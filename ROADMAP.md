# Roadmap

## 🟢 Phase 1: Recovery & Infrastructure (Completed)
- [x] Recover files from 2014 archive.
- [x] Convert legacy documents to Markdown (`WORLD_CODEX.md`).
- [x] Establish functional hierarchy (`01_Design_Sources`, `02_Visual_Assets`, etc.).
- [x] Extract to standalone public repository.
- [x] Unified "Kaelia" naming convention.

## 🟢 Phase 2: Lore & Identity (Completed)
- [x] **Modern-Ancient Synthesis:** Established the definitive tech/cultural premise.
- [x] **Wiki Expansion:** Full entries for all 37 states and regions in `WORLD_CODEX.md`.
- [x] **Visual Prompting:** High-fidelity AI prompt library for every geopolitical entity.
- [x] **Asset Framework:** 1:1 directory structure for all regional visuals.
- [x] **Biome-Correction Audit:** Unified all geography and climate data with Whittaker Classification (v2.1).
- [x] **Licensing:** Secured under CC BY-NC-SA 4.0.

## 🟡 Phase 3: Visual & Interactive Expansion (Current Focus)
- [x] **Modern Map Viewer:** Full "Google Maps" refactor (Search, Sidebar, Zoom-Labels).
- [x] **Frontier Extraction:** Successfully extracted and refined transparent overlays for political boundaries.
- [x] **Altitude Integration:** High-fidelity 16-bit terrain mapping and precise city elevation tracking.
- [x] **Heraldry System:** Implementation of mottos, descriptions, and UI integration for all entities.
- [x] **NorKunta Expansion:** Detailed lore and visuals for Northern Antarmund (Cryo-Vault 09, Koldfisk, Borealis).
- [x] **Interactive Encyclopedia:** Generated multi-page HTML wiki linked to Map Viewer (Dark Mode + Lightbox).
- [x] **Heraldry Prompts:** Created batch prompt library for flags and coats of arms (`heraldry_prompts.md`).
- [x] **Image Carousel System:** Multi-image carousel in the Map Viewer sidebar and wiki city profiles. Dynamic `/api/city-images` endpoint.
- [x] **Climate Legend:** Toggle-able Leaflet legend control for the Climate layer.
- [x] **Data Consolidation:** Flattened world hierarchy to a clean 3-tier structure (Continent → Country → City). Consolidated Betereko. Fixed Map Viewer crash (Pelak invalid type). Regenerated wiki for 36 countries and 61 cities.
- [x] **AI Asset Generation:** Batch generation of flags, coats of arms, and regional landscape cards (Hybrid Pipeline Active).
- [x] **3D Globe View:** Interactive `globe.gl` integration with 2D/3D toggle FAB, auto-rotate, and city markers.
- [x] **Generation API:** Server-side `/api/generate-visual` and `/api/construct-prompt` endpoints with automatic file management and heraldry archiving.
- [x] **Asset Auditor:** Automated asset-existence validation (`check_assets.js`) producing filesystem reports.
- [x] **Movable Labels:** Draggable Continent and Country labels with persistent coordinate storage.
- [x] **Prompt Explorer:** Dedicated tool for viewing, searching, and analyzing AI prompts per city. **V2 Update:** Added Filtering, Deep Linking (`?cityId`), City Editing, and On-Demand Generation.
- [x] **City Editing:** Direct modification of city data (Population, Lore, JSON) via UI.
- [x] **Wiki Synchronization:** Automated HTML updates and fixed path resolution bugs.
- [x] **Navigation Integration:** Direct deep-linking from Map Viewer "Edit" button to Prompt Explorer.
- [x] **UI Cleanup:** Removed legacy generation buttons to declutter main interfaces.
- [ ] **AI Upscaling:** Remaster legacy renders and maps to 4K.
- [ ] **3D Porting:** Port `.c4d` models to Blender for modern PBR rendering.

## 🔵 Phase 4: Narrative Release
- [ ] **Short Stories:** First anthology set in the high-tech fjords of Gryning.
- [ ] **Timeline:** Document the historical evolution of the Modern-Ancient Synthesis.
- [ ] **Interactive Guide:** Web-based interactive version of the `WORLD_CODEX.md`.
