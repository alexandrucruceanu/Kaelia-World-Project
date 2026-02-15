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

    if (req.url === '/api/generate-visual' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            const { cityId, model } = JSON.parse(body);
            const { spawn } = require('child_process');
            
            console.log(`🎨 Generating visual for ${cityId} using ${model}...`);

            // Path to python script
            const pythonScript = path.join(__dirname, 'scripts', 'generate_assets_hybrid.py');
            
            // Spawn python process
            const pythonProcess = spawn('python', [pythonScript, '--id', cityId, '--model', model, '--type', 'landscape']);
            
            let stdoutData = '';
            let stderrData = '';

            pythonProcess.stdout.on('data', (data) => {
                stdoutData += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                stderrData += data.toString();
                console.error(`Python Error: ${data}`);
            });

            pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: 'Script failed', details: stderrData }));
                } else {
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    // Expecting JSON from stdout
                    try {
                        // The script might print other things, so we need to be careful.
                        // Ideally the script ONLY prints JSON.
                        // Let's trim whitespace and try to parse.
                        const jsonResponse = JSON.parse(stdoutData.trim());
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

            // Construct Path
            // Structure: assets/images/{Continent}/{Country}/{City}/
            
            const safeCont = tContinent.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_');
            const safeCount = tCountry.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_');
            const safeCity = targetCity.name.split('').filter(x => /[a-zA-Z0-9 _-]/.test(x)).join('').trim().replace(/ /g, '_').toLowerCase();

            const imagesDir = path.join(__dirname, 'assets', 'images', safeCont, safeCount, safeCity);
            
            fs.readdir(imagesDir, (err, files) => {
                if (err) {
                    // Directory might not exist yet if no images
                    return res.end(JSON.stringify([]));
                }
                
                // Filter images
                // Sort: main first, then by number
                const images = files
                    .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
                    .sort((a, b) => {
                        if (a.includes('_main')) return -1;
                        if (b.includes('_main')) return 1;
                        // Extract number if possible
                        // name_1.png vs name_2.png
                        const gam = a.match(/_(\d+)\./);
                        const gbm = b.match(/_(\d+)\./);
                        if (gam && gbm) return parseInt(gam[1]) - parseInt(gbm[1]);
                        return a.localeCompare(b);
                    })
                    .map(f => `/assets/images/${safeCont}/${safeCount}/${safeCity}/${f}`);
                
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
