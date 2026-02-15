const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data', 'master_world_data.json');

const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
};

const server = http.createServer((req, res) => {
    // API Endpoints
    if (req.url === '/api/world' && req.method === 'GET') {
        fs.readFile(DATA_FILE, 'utf8', (err, data) => {
            if (err) {
                res.writeHead(500);
                return res.end('Error reading data');
            }
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(data);
        });
        return;
    }

    if (req.url === '/api/cities' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            const { continentName, countryName, city } = JSON.parse(body);
            fs.readFile(DATA_FILE, 'utf8', (err, data) => {
                if (err) {
                    res.writeHead(500);
                    return res.end('Error reading data');
                }
                const world = JSON.parse(data);
                const continent = world.continents.find(c => c.name === continentName);
                if (!continent) {
                    res.writeHead(404);
                    return res.end('Continent not found');
                }
                const country = continent.countries.find(c => c.name === countryName);
                if (!country) {
                    res.writeHead(404);
                    return res.end('Country not found');
                }
                
                // Generate simple unique ID
                const timestamp = Date.now();
                city.id = `city_${timestamp}`;
                
                country.cities.push(city);
                fs.writeFile(DATA_FILE, JSON.stringify(world, null, 2), (err) => {
                    if (err) {
                        res.writeHead(500);
                        return res.end('Error saving data');
                    }
                    res.writeHead(201, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(city));
                });
            });
        });
        return;
    }

    if (req.url === '/api/cities' && req.method === 'PUT') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            const { continentName, countryName, city } = JSON.parse(body);
            fs.readFile(DATA_FILE, 'utf8', (err, data) => {
                if (err) {
                    res.writeHead(500);
                    return res.end('Error reading data');
                }
                const world = JSON.parse(data);
                let found = false;
                
                // Search and update by ID
                world.continents.forEach(continent => {
                    continent.countries.forEach(country => {
                        const index = country.cities.findIndex(c => c.id === city.id);
                        if (index !== -1) {
                            country.cities[index] = city;
                            found = true;
                        }
                    });
                });

                if (!found) {
                    res.writeHead(404);
                    return res.end('City not found');
                }
                
                fs.writeFile(DATA_FILE, JSON.stringify(world, null, 2), (err) => {
                    if (err) {
                        res.writeHead(500);
                        return res.end('Error saving data');
                    }
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(city));
                });
            });
        });
        return;
    }

    // --- Construct Prompt Endpoint ---
    if (req.url === '/api/construct-prompt' && req.method === 'POST') {
        console.log('📝 /api/construct-prompt called');
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            const { cityId, genType } = JSON.parse(body);
            const { spawn } = require('child_process');
            const pythonScript = path.join(__dirname, 'scripts', 'generate_assets_hybrid.py');
            const pyType = (genType === 'heraldry_flag') ? 'flag' : (genType === 'heraldry_arms') ? 'arms' : 'landscape';
            
            const pyProcess = spawn('python', [pythonScript, '--id', cityId, '--type', pyType, '--construct-only']);
            let stdoutData = '';
            pyProcess.stdout.on('data', d => { stdoutData += d.toString(); });
            pyProcess.stderr.on('data', d => { console.error(`Prompt construct error: ${d}`); });
            pyProcess.on('close', (code) => {
                res.writeHead(code === 0 ? 200 : 500, { 'Content-Type': 'application/json' });
                try {
                    res.end(stdoutData.trim());
                } catch(e) {
                    res.end(JSON.stringify({ status: 'error', message: 'Failed to construct prompt' }));
                }
            });
        });
        return;
    }

    // --- Generate Visual Endpoint (expanded) ---
    if (req.url === '/api/generate-visual' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            const { cityId, model, genType, prompt } = JSON.parse(body);
            // genType: "landscape_main" | "landscape_seq" | "heraldry_flag" | "heraldry_arms"
            const { spawn } = require('child_process');
            
            console.log(`🎨 Generating ${genType} for ${cityId} using ${model}...`);

            // Load world data first for file management
            let worldData;
            try {
                worldData = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
            } catch(e) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                return res.end(JSON.stringify({ status: 'error', message: 'Failed to read world data' }));
            }

            // Find entity
            let targetCity = null, tCountry = null, tContinent = null;
            for (const cont of worldData.continents) {
                for (const country of cont.countries) {
                    for (const city of country.cities) {
                        if (city.id === cityId) {
                            targetCity = city; tCountry = country.name; tContinent = cont.name;
                        }
                    }
                }
            }
            if (!targetCity) {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                return res.end(JSON.stringify({ status: 'error', message: 'City not found' }));
            }

            // --- File Management (pre-generation) ---
            const safeName = (t) => t.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_');
            const safeCity = safeName(targetCity.name).toLowerCase();
            let outputPath = null;  // Will be set if we need specific output
            let pyType = 'landscape';

            if (genType === 'landscape_main') {
                // If main exists, rename to next sequence number
                const imgDir = targetCity.image ? path.join(__dirname, path.dirname(targetCity.image)) :
                    path.join(__dirname, 'assets', 'images', safeName(tContinent), safeName(tCountry), safeCity);
                const mainFile = path.join(imgDir, `${safeCity}_main.png`);
                
                if (fs.existsSync(mainFile)) {
                    // Find next sequence number
                    let idx = 1;
                    while (fs.existsSync(path.join(imgDir, `${safeCity}_${idx}.png`))) idx++;
                    const seqFile = path.join(imgDir, `${safeCity}_${idx}.png`);
                    fs.renameSync(mainFile, seqFile);
                    console.log(`  📁 Moved old main to ${path.basename(seqFile)}`);
                }
                // Output to main
                if (!fs.existsSync(imgDir)) fs.mkdirSync(imgDir, { recursive: true });
                outputPath = mainFile;
                pyType = 'landscape';

            } else if (genType === 'landscape_seq') {
                // Just find next sequence slot
                const imgDir = targetCity.image ? path.join(__dirname, path.dirname(targetCity.image)) :
                    path.join(__dirname, 'assets', 'images', safeName(tContinent), safeName(tCountry), safeCity);
                if (!fs.existsSync(imgDir)) fs.mkdirSync(imgDir, { recursive: true });
                let idx = 1;
                while (fs.existsSync(path.join(imgDir, `${safeCity}_${idx}.png`))) idx++;
                outputPath = path.join(imgDir, `${safeCity}_${idx}.png`);
                pyType = 'landscape';

            } else if (genType === 'heraldry_flag' || genType === 'heraldry_arms') {
                const sub = genType === 'heraldry_flag' ? 'flags' : 'arms';
                const heraldryFile = path.join(__dirname, 'assets', 'heraldry', sub, `city_${safeCity}.png`);
                
                // Archive old heraldry if it exists
                if (fs.existsSync(heraldryFile)) {
                    const archiveDir = path.join(__dirname, 'assets', 'heraldry', '_archive', sub);
                    if (!fs.existsSync(archiveDir)) fs.mkdirSync(archiveDir, { recursive: true });
                    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0,19);
                    const archiveName = `city_${safeCity}_${timestamp}.png`;
                    fs.renameSync(heraldryFile, path.join(archiveDir, archiveName));
                    console.log(`  📦 Archived old ${sub} to _archive/${sub}/${archiveName}`);
                }
                outputPath = heraldryFile;
                pyType = genType === 'heraldry_flag' ? 'flag' : 'arms';
            }

            // Build Python command
            const pythonScript = path.join(__dirname, 'scripts', 'generate_assets_hybrid.py');
            const pyArgs = [pythonScript, '--id', cityId, '--model', model, '--type', pyType];
            if (prompt) { pyArgs.push('--prompt', prompt); }
            if (outputPath) { pyArgs.push('--output', outputPath); }
            
            // Spawn python process
            const pythonProcess = spawn('python', pyArgs);
            let stdoutData = '';
            let stderrData = '';

            pythonProcess.stdout.on('data', (data) => { stdoutData += data.toString(); });
            pythonProcess.stderr.on('data', (data) => {
                stderrData += data.toString();
                console.error(`Python: ${data}`);
            });

            pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: 'Script failed', details: stderrData }));
                } else {
                    try {
                        const jsonResponse = JSON.parse(stdoutData.trim());
                        
                        // Post-generation: update JSON data if needed
                        if (jsonResponse.status === 'success') {
                            // Update image path in world data for landscape_main
                            if (genType === 'landscape_main' && jsonResponse.image_path) {
                                targetCity.image = jsonResponse.image_path;
                                fs.writeFileSync(DATA_FILE, JSON.stringify(worldData, null, 2));
                                console.log(`  ✅ Updated city image path to ${jsonResponse.image_path}`);
                            }
                            // Update heraldry path in world data
                            if (genType === 'heraldry_flag' && jsonResponse.image_path) {
                                if (!targetCity.heraldry) targetCity.heraldry = {};
                                targetCity.heraldry.flag = '/' + jsonResponse.image_path;
                                fs.writeFileSync(DATA_FILE, JSON.stringify(worldData, null, 2));
                                console.log(`  ✅ Updated city flag path`);
                            }
                            if (genType === 'heraldry_arms' && jsonResponse.image_path) {
                                if (!targetCity.heraldry) targetCity.heraldry = {};
                                targetCity.heraldry.coat_of_arms = '/' + jsonResponse.image_path;
                                fs.writeFileSync(DATA_FILE, JSON.stringify(worldData, null, 2));
                                console.log(`  ✅ Updated city coat_of_arms path`);
                            }
                        }
                        
                        res.writeHead(200, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify(jsonResponse));
                    } catch (e) {
                         res.writeHead(500, { 'Content-Type': 'application/json' });
                         res.end(JSON.stringify({ status: 'error', message: 'Invalid JSON from script', output: stdoutData }));
                    }
                }
            });
        });
        return;
    }

    if (req.url.startsWith('/api/city-images') && req.method === 'GET') {
        // Parse query params manually or use URL object
        const urlObj = new URL(req.url, `http://${req.headers.host}`);
        const cityId = urlObj.searchParams.get('cityId');
        
        if (!cityId) {
             res.writeHead(400);
             return res.end('Missing cityId');
        }

        // We need to look up the city to get path details
        fs.readFile(DATA_FILE, 'utf8', (err, data) => {
            if (err) { res.writeHead(500); return res.end('Error reading data'); }
            
            const world = JSON.parse(data);
            let targetCity = null; 
            let tContinent = null;
            let tCountry = null;

            // Flatten search
            for (const cont of world.continents) {
                for (const count of cont.countries) {
                    const c = count.cities.find(ct => ct.id === cityId);
                    if (c) { targetCity = c; tContinent = cont.name; tCountry = count.name; break; }
                }
                if (targetCity) break;
            }

            if (!targetCity) { res.writeHead(404); return res.end('City not found'); }

            // Derive image directory from the city's image path property
            let imagesDir;
            if (targetCity.image) {
                // image is like "assets/images/Antarmund/NorKunta/jarnhofn/jarnhofn_main.png"
                const imageRelDir = path.dirname(targetCity.image);
                imagesDir = path.join(__dirname, imageRelDir);
            } else {
                // Fallback: construct path from names (ASCII-safe)
                const safeCont = tContinent.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_');
                const safeCount = tCountry.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_');
                const safeCity = targetCity.name.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_').toLowerCase();
                imagesDir = path.join(__dirname, 'assets', 'images', safeCont, safeCount, safeCity);
            }
            // Derive URL prefix from imagesDir (relative to __dirname)
            const relDir = path.relative(__dirname, imagesDir).replace(/\\/g, '/');

            fs.readdir(imagesDir, (err, files) => {
                if (err) {
                    // Directory might not exist yet if no images
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    return res.end(JSON.stringify([]));
                }
                
                // Filter images
                // Sort: main first, then by number
                const images = files
                    .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
                    .sort((a, b) => {
                        if (a.includes('_main')) return -1;
                        if (b.includes('_main')) return 1;
                        const gam = a.match(/_(\d+)\./);
                        const gbm = b.match(/_(\d+)\./);
                        if (gam && gbm) return parseInt(gam[1]) - parseInt(gbm[1]);
                        return a.localeCompare(b);
                    })
                    .map(f => `/${relDir}/${f}`);
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(images));
            });
        });
        return;
    }

    // Static File Serving
    console.log(`Serving: ${req.url}`); // Debug logging
    let filePath = '.' + req.url;
    if (filePath === './') filePath = './index.html';

    const extname = String(path.extname(filePath)).toLowerCase();
    const contentType = MIME_TYPES[extname] || 'application/octet-stream';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code == 'ENOENT') {
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end('Sorry, check with the site admin for error: ' + error.code + ' ..\n');
            }
        } else {
            res.writeHead(200, { 
                'Content-Type': contentType,
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            });
            res.end(content);
        }
    });
});

server.listen(PORT, () => {
    console.log(`Kaelia Map Server (Zero-Dep) running at http://localhost:${PORT}`);
});
