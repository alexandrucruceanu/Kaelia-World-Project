const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data', 'world_data.json');

const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
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

    // Static File Serving
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
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`Kaelia Map Server (Zero-Dep) running at http://localhost:${PORT}`);
});
