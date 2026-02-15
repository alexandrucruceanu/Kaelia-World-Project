const fs = require('fs');
const path = require('path');

// Paths
const DATA_DIR = path.join(__dirname, '../data');
const PROJECT_ROOT = path.join(__dirname, '../../../../'); 
const WORLD_DATA_PATH = path.join(DATA_DIR, 'world_data.json');
const MASTER_DATA_PATH = path.join(DATA_DIR, 'master_world_data.json');
const CODEX_PATH = path.join(PROJECT_ROOT, 'World_Building_Project', 'WORLD_CODEX.md');
const PROMPTS_PATH = path.join(PROJECT_ROOT, 'World_Building_Project', 'IMAGE_GENERATION_PROMPTS.md');
const LOG_PATH = path.join(DATA_DIR, 'migration_log.txt');

function log(msg) {
    fs.appendFileSync(LOG_PATH, msg + '\n');
    console.log(msg); // Keep console for basic status
}

// Clear log
fs.writeFileSync(LOG_PATH, '');

// 1. Load Base Data
log(`Loading base data from ${WORLD_DATA_PATH}...`);
if (!fs.existsSync(WORLD_DATA_PATH)) {
    log("Error: world_data.json not found!");
    process.exit(1);
}
const worldData = JSON.parse(fs.readFileSync(WORLD_DATA_PATH, 'utf8'));

// 2. Parse WORLD_CODEX.md
log(`Parsing Lore from ${CODEX_PATH}...`);
let loreMap = {};
if (fs.existsSync(CODEX_PATH)) {
    const codexContent = fs.readFileSync(CODEX_PATH, 'utf8');
    const lines = codexContent.split('\n');
    let currentContinent = null;
    let currentRegion = null;

    lines.forEach(line => {
        // Simple heuristic parsing
        const continentMatch = line.match(/^## .* Continent \d+: (.*)/);
        const regionMatch = line.match(/^### \d+\. (.*)/);
        
        // Extract bullet points that look like locations: * **Name:** Description
        // Allow leading whitespace
        const locationMatch = line.match(/^\s*\*\s*\*\*([^*]+)\*\*(.*)/);

        if (continentMatch) {
            currentContinent = continentMatch[1].trim();
        } else if (regionMatch) {
            currentRegion = regionMatch[1].trim();
            loreMap[currentRegion] = { type: 'region', desc: '' }; // Placeholder
        } else if (locationMatch) {
            let name = locationMatch[1].trim();
            let desc = locationMatch[2].replace(/^: - /, '').replace(/^: /, '').trim();
            
            // Special handling for Metropolis line: * **Metropolis:** **CityName** ...
            if (name === 'Metropolis' || name === 'Capital') {
                const cityMatch = desc.match(/^\s*\*\*([^*]+)\*\*/);
                if (cityMatch) {
                    name = cityMatch[1].trim(); // Extract Skýjakot
                    desc = desc.substring(cityMatch[0].length).replace(/^ - /, '').replace(/^: /, '').trim();
                }
            }

            if (name.endsWith(':')) name = name.slice(0, -1);
            
            // Filter out obviously wrong keys like "Location", "Visual Biome"
            if (!['Location', 'Visual Biome', 'Geography', 'Culture', 'Modern', 'Conflict', 'Settlements', 'Villages', 'Islands', 'Anomalies'].includes(name)) {
                loreMap[name] = {
                    desc: desc,
                    source: 'WORLD_CODEX.md'
                };
            }
        }
    });
} else {
    log("Warning: WORLD_CODEX.md not found.");
}

// 3. Parse IMAGE_GENERATION_PROMPTS.md
log(`Parsing Prompts from ${PROMPTS_PATH}...`);
let promptMap = {};
if (fs.existsSync(PROMPTS_PATH)) {
    const promptsContent = fs.readFileSync(PROMPTS_PATH, 'utf8');
    const sections = promptsContent.split('\n### ');
    
    sections.forEach(section => {
        if (!section.trim()) return;

        // Capture full line for name to find aliases in parens
        const nameMatch = section.match(/^\d+\.\s+(.*)/);
        if (!nameMatch) return; 
        
        let name = nameMatch[1].trim();
        
        const promptMatch = section.match(/> \*Prompt:\* ([\s\S]*?)(?=\n\n|\n```)/);
        const promptText = promptMatch ? promptMatch[1].trim().replace(/\n/g, ' ') : null;

        // Extract JSON - look for code block
        const jsonMatch = section.match(/```json\s*([\s\S]*?)```/);
        let promptJson = null;
        if (jsonMatch) {
            try {
                promptJson = JSON.parse(jsonMatch[1]);
            } catch (e) {
                log(`Failed to parse JSON for ${name}: ${e.message}`);
            }
        }

        if (promptText || promptJson) {
            promptMap[name] = {
                prompt: promptText,
                schema: promptJson
            };
        }
    });
} else {
    log("Warning: IMAGE_GENERATION_PROMPTS.md not found.");
}

// Debug matching
log(`Loaded ${Object.keys(loreMap).length} Lore entries.`);
log(`Lore Keys Sample: ${Object.keys(loreMap).slice(0, 10).join(', ')}`);
log(`Loaded ${Object.keys(promptMap).length} Prompt entries.`);
log(`Prompt Keys Sample: ${Object.keys(promptMap).slice(0, 10).join(', ')}`);

// Helper: Fuzzy Matcher
function findMatch(name, map) {
    if (!name) return null;
    if (map[name]) return map[name];
    
    const cleanName = name.replace(/\s*\(.*\)/, '').trim();
    // Try finding key that CONTAINS name or vice versa
    for (const key in map) {
        // Check raw key first (for cases like "Gryning (... Skýjakot ...)")
        if (key.includes(name)) return map[key];

        const cleanKey = key.replace(/\s*\(.*\)/, '').trim();
        // Exact match after cleaning
        if (cleanKey === name || cleanKey === cleanName) return map[key];
        
        // Substring match - be careful with short names
        if (name.length > 3 && cleanKey.includes(name)) return map[key];
        if (cleanKey.length > 3 && name.includes(cleanKey)) return map[key];
    }
    return null;
}

// 3.5. Asset Migration Logic
const VISUALS_ROOT = path.join(PROJECT_ROOT, 'World_Building_Project', '02_Visual_Assets');
const ASSETS_DEST = path.join(__dirname, '../assets/images');

// Ensure destination exists
if (!fs.existsSync(ASSETS_DEST)) {
    fs.mkdirSync(ASSETS_DEST, { recursive: true });
}

// Map of found images: normalizedName -> fullPath
let imageMap = {};

function scanForImages(dir) {
    if (!fs.existsSync(dir)) return;
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            scanForImages(fullPath);
        } else if (file.match(/\.(png|jpg|jpeg|webp)$/i)) {
            // Clean name: "NorKunta Prime.png" -> "NorKunta Prime"
            const name = path.parse(file).name;
            imageMap[name] = fullPath;
            // Also store normalized version? "norkuntaprime" -> path
            imageMap[name.toLowerCase().replace(/[^a-z0-9]/g, '')] = fullPath;
        }
    });
}

log(`Scanning for images in ${VISUALS_ROOT}...`);
scanForImages(VISUALS_ROOT);
log(`Found ${Object.keys(imageMap).length} potential image assets.`);

// 4. Merge Data
log("Merging data...");

worldData.continents.forEach(cont => {
    cont.countries.forEach(country => {
        country.cities.forEach(city => {
            // Debug specific city
            if (city.name === 'Hafnir' || city.name === 'Skýjakot') {
               log(`Checking city: ${city.name}`);
               log(`Lore match: ${findMatch(city.name, loreMap) ? 'FOUND' : 'NOT FOUND'}`);
               log(`Prompt match: ${findMatch(city.name, promptMap) ? 'FOUND' : 'NOT FOUND'}`);
            }

            const lore = findMatch(city.name, loreMap);
            if (lore) {
                city.lore = lore;
            }
            // Merge Prompts
            const visual = findMatch(city.name, promptMap);
            if (visual) {
                city.visual_data = visual;
            }

            // Link Assets
            // Try direct match first
            let imagePath = imageMap[city.name];
            // Try normalized match
            if (!imagePath) {
                 const normalized = city.name.toLowerCase().replace(/[^a-z0-9]/g, '');
                 imagePath = imageMap[normalized];
            }

            if (imagePath) {
                // Calculate relative path from source root to preserve structure
                // e.g. "Nordica\Gryning\Skýjakot.png"
                const relativePath = path.relative(VISUALS_ROOT, imagePath);
                const destPath = path.join(ASSETS_DEST, relativePath);
                
                // Ensure destination directory exists
                const destDir = path.dirname(destPath);
                if (!fs.existsSync(destDir)) {
                    fs.mkdirSync(destDir, { recursive: true });
                }

                // Copy file
                try {
                    fs.copyFileSync(imagePath, destPath);
                    // Use forward slashes for URL/JSON
                    city.image = `assets/images/${relativePath.replace(/\\/g, '/')}`; 
                    // log(`Linked image for ${city.name}`);
                } catch (e) {
                    log(`Error copying image for ${city.name}: ${e.message}`);
                }
            }
        });
    });
});

// 5. Write Master Data
fs.writeFileSync(MASTER_DATA_PATH, JSON.stringify(worldData, null, 2));
log(`Success! Master database written to ${MASTER_DATA_PATH}`);
