var map = L.map('map', {
    crs: L.CRS.Simple, minZoom: -2, maxZoom: 2, zoomSnap: 0.5, zoomDelta: 0.5,
    zoomControl: false // We will move it or use custom logic later
});

L.control.zoom({ position: 'bottomright' }).addTo(map); // Move zoom to bottom right

var bounds = [[0,0], [1000,2000]];
var satLayer = L.imageOverlay('img/satellite.jpg', bounds);
var polLayer = L.imageOverlay('img/political.jpg', bounds);
var altLayer = L.imageOverlay('img/altitude.jpg', bounds);

var categoryConfig = {
    capital: { radius: 12, weight: 4, opacity: 1, fillOpacity: 1, label: "🏛️ Capital", badge: "Capital City" },
    metropolis: { radius: 10, weight: 3, opacity: 1, fillOpacity: 0.9, label: "🏙️ Metropolis", badge: "Metropolis" },
    settlement: { radius: 7, weight: 2, opacity: 1, fillOpacity: 0.7, label: "🏡 Settlement", badge: "Settlement" },
    village: { radius: 5, weight: 1, opacity: 0.8, fillOpacity: 0.6, label: "🏕️ Village", badge: "Village" },
    special: { radius: 8, weight: 2, opacity: 1, fillOpacity: 0.8, label: "🔬 Special", badge: "Special Site" }
};

var layers = {
    capital: L.layerGroup(), metropolis: L.layerGroup(), settlement: L.layerGroup(), village: L.layerGroup(), special: L.layerGroup()
};

var gridLayer = L.layerGroup();
var frontiersOverlay = L.imageOverlay('data/frontiers_overlay.png', bounds, { opacity: 1.0, interactive: false });
var politicalComposite = L.layerGroup([satLayer, frontiersOverlay]);

var worldData = {};
var currentCity = null; // Currently selected city
var moveMode = false;
var addMode = false;
var tempMarker = null; // Marker for adding new loc

// --- Initialization ---
// --- Initialization ---
// (Moved to bottom of file)
    

// --- Data Loading ---
function loadMarkers() {
    Object.values(layers).forEach(layer => layer.clearLayers());

    fetch('/api/world')
        .then(res => res.json())
        .then(data => {
            worldData = data;
            populateHierarchy(); // Populate dropdowns
            
            data.continents.forEach(continent => {
                continent.countries.forEach(country => {
                    country.cities.forEach(city => {
                        createMarker(city, continent.name, country.name);
                    });
                });
            });
        });
}

function createMarker(city, continentName, countryName) {
    var config = categoryConfig[city.type] || categoryConfig.settlement;
    
    // Style marker
    var markerIcon = L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="background-color: ${city.color || '#ea4335'}; width: ${config.radius * 2}px; height: ${config.radius * 2}px; border-radius: 50%; border: 2px solid white; box-shadow: 0 1px 3px rgba(0,0,0,0.5);" class="map-marker-circle"></div>`,
        iconSize: [config.radius * 2, config.radius * 2],
        iconAnchor: [config.radius, config.radius]
    });

    var marker = L.marker(city.coords, {
        icon: markerIcon,
        draggable: false, // Default false, toggled by Move Mode
        id: city.id
    });

    // Tooltip (Label)
    marker.bindTooltip(city.name, { 
        permanent: true, direction: 'bottom', className: `city-label label-${city.type}`, offset: [0, 8] 
    });

    // Interaction
    marker.on('click', () => openSidebarDetails(city, continentName, countryName));
    
    // Drag Logic (if enabled later)
    marker.on('dragend', function(e) {
        if (!moveMode) return;
        var newCoords = [parseFloat(e.target.getLatLng().lat.toFixed(1)), parseFloat(e.target.getLatLng().lng.toFixed(1))];
        city.coords = newCoords;
        
        // Auto-Update Data on Move
        city.climate = getClimateAt(newCoords[0], newCoords[1]);
        // city.altitude = getAltitudeAt(newCoords[0], newCoords[1]); // Optional if added to schema
        
        updateCityOnServer(continentName, countryName, city);
        openSidebarDetails(city, continentName, countryName); // Update stats
    });

    marker.activeReference = { city, continentName, countryName }; // Store Ref
    marker.addTo(layers[city.type]);
}

// --- UI Logic: Sidebar ---
function openSidebar() {
    document.getElementById('sidebar').classList.add('open');
}
function closeSidebar() {
    document.getElementById('sidebar').classList.remove('open');
    currentCity = null;
    map.closePopup(); // Should handle map deselect logic
}

function openSidebarDetails(city, continentName, countryName) {
    currentCity = { city, continentName, countryName };
    
    // Switch to Details View
    document.getElementById('sidebar-form').classList.remove('active');
    document.getElementById('sidebar-details').classList.add('active');
    
    // Populate Data
    document.getElementById('detail-title').innerText = city.name;
    document.getElementById('detail-type').innerText = categoryConfig[city.type]?.badge || city.type;
    document.getElementById('detail-desc').innerText = city.desc || "No description available.";

    // Header Image
    const bgElement = document.getElementById('detail-bg');
    if (city.image) {
        bgElement.src = city.image;
    } else {
        bgElement.src = "img/satellite.jpg";
    }

    // Population Display
    const popRow = document.getElementById('detail-pop-row');
    if (city.population) {
        document.getElementById('detail-pop').innerText = city.population;
        popRow.style.display = 'flex';
    } else {
        popRow.style.display = 'none';
    }
    document.getElementById('detail-coords').innerText = city.coords.join(', ');
    document.getElementById('detail-climate').innerText = city.climate || getClimateAt(city.coords[0], city.coords[1]);
    document.getElementById('detail-altitude').innerText = city.altitude || getAltitudeAt(city.coords[0], city.coords[1]);
    document.getElementById('detail-region').innerText = `${countryName}, ${continentName}`;
    
    // Heraldry Display
    const heraldry = city.heraldry || {};
    const mottoEl = document.getElementById('detail-motto');
    const hDescEl = document.getElementById('detail-heraldry-desc');
    const flagImg = document.getElementById('detail-flag');
    const armsImg = document.getElementById('detail-arms');

    if (heraldry.motto) {
        mottoEl.innerText = `"${heraldry.motto}"`;
        hDescEl.innerText = heraldry.description || "";
        
        if (heraldry.flag) {
            flagImg.src = heraldry.flag;
            flagImg.style.display = 'block';
        } else {
            flagImg.style.display = 'none';
        }

        if (heraldry.coat_of_arms) {
            armsImg.src = heraldry.coat_of_arms;
            armsImg.style.display = 'block';
        } else {
            armsImg.style.display = 'none';
        }
        document.getElementById('heraldry-section').style.display = 'block';
    } else {
        document.getElementById('heraldry-section').style.display = 'none';
    }
    
    // Lore Display
    const loreContainer = document.getElementById('detail-lore-container');
    const loreText = document.getElementById('detail-lore');
    if (city.lore && city.lore.desc) {
        loreText.innerText = city.lore.desc;
        loreContainer.style.display = 'block';
    } else {
        loreContainer.style.display = 'none';
    }

    // Visual Data Display
    const visContainer = document.getElementById('detail-visuals-container');
    if (city.visual_data) {
        visContainer.style.display = 'block';
        document.getElementById('detail-prompt').innerText = city.visual_data.prompt || "No text prompt.";
        
        const schemaDiv = document.getElementById('detail-schema');
        if (city.visual_data.schema && city.visual_data.schema.meta) {
                 const meta = city.visual_data.schema.meta;
                 const context = city.visual_data.schema.global_context || {};
                 schemaDiv.innerHTML = `
                    <div style="display:grid; grid-template-columns: auto 1fr; gap: 4px;">
                        <span style="color:#202124;">Type:</span> <span>${meta.image_type || '-'}</span>
                        <span style="color:#202124;">Ratio:</span> <span>${meta.aspect_ratio || '-'}</span>
                        <span style="color:#202124;">Lighting:</span> <span>${context.lighting || '-'}</span>
                        <span style="color:#202124;">Mood:</span> <span>${context.atmosphere || '-'}</span>
                    </div>
                `;
        } else {
            schemaDiv.innerHTML = '';
        }
        
        // Populate Raw JSON
        const jsonPre = document.getElementById('detail-json');
        if (city.visual_data.schema) {
            jsonPre.innerText = JSON.stringify(city.visual_data.schema, null, 2);
        } else {
            jsonPre.innerText = "No JSON schema available.";
        }
    } else {
        visContainer.style.display = 'none';
    }
    
    // Show Edit Button
    document.getElementById('btn-edit-loc').style.display = 'flex';
    document.getElementById('btn-edit-loc').onclick = () => openSidebarEdit(city, continentName, countryName);
    
    openSidebar();
}

function openSidebarEdit(city = null, continentName = null, countryName = null) {
    // Switch to Form View
    document.getElementById('sidebar-details').classList.remove('active');
    document.getElementById('sidebar-form').classList.add('active');
    
    if (city) {
        // Edit Mode
        document.querySelector('.form-header h2').innerText = "Edit Location";
        document.getElementById('edit-name').value = city.name;
        document.getElementById('edit-type').value = city.type;
        document.getElementById('edit-coords').value = city.coords.join(', ');
        document.getElementById('edit-pop').value = city.population || "";
        document.getElementById('edit-climate').value = city.climate || getClimateAt(city.coords[0], city.coords[1]); // Use existing or detect
        document.getElementById('edit-desc').value = city.desc;
        
        setDropdowns(continentName, countryName);
    } else {
        // Add Mode
        document.querySelector('.form-header h2').innerText = "Add Location";
        document.getElementById('edit-name').value = "";
        document.getElementById('edit-desc').value = "";
        document.getElementById('edit-pop').value = "";
        document.getElementById('edit-climate').value = "Click map to detect";
        // Coords should be set by click map logic
    }
    
    openSidebar();
}

// --- Climate Detection Logic ---
var climateContext = null;
var climateMapData = null;
var mapWidth = 6000; // Intrinsic size of the map image
var mapHeight = 3000;

// Approximate Whittaker / Map Colors (Standardized)
// User can Calibrate this by logging clicks if needed.
var colorToClimate = [
    { name: "Polar Ice Cap", color: [255, 255, 255] }, // White
    { name: "Tundra / Alpine", color: [160, 210, 230] }, // Light Blue-Grey
    { name: "Boreal Forest (Taiga)", color: [0, 90, 80] }, // Dark Teal
    { name: "Temperate Rainforest", color: [30, 160, 80] }, // Lush Green
    { name: "Temperate Seasonal Forest", color: [100, 200, 100] }, // Medium Green
    { name: "Tropical Rainforest", color: [0, 60, 0] }, // Deep Dark Green
    { name: "Tropical Seasonal Forest", color: [50, 100, 30] }, // Olive Green
    { name: "Savanna", color: [200, 220, 100] }, // Yellow-Green
    { name: "Subtropical Desert", color: [255, 230, 100] }, // Sand Yellow
    { name: "Cold Desert", color: [180, 180, 180] }, // Grey
    { name: "Chaparral / Mediterranean", color: [180, 150, 50] }, // Brownish Green
    { name: "Ocean", color: [20, 40, 90] } // Deep Blue (Mask out)
];

function initClimateMap() {
    var canvas = document.getElementById('climate-canvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    var img = new Image();
    img.src = 'data/climate_map.jpg';
    img.onload = function() {
        canvas.width = mapWidth;
        canvas.height = mapHeight;
        ctx.drawImage(img, 0, 0, mapWidth, mapHeight);
        climateContext = ctx;
        console.log("Climate Map Loaded & Rasterized.");
    };
    img.onerror = function() {
        console.error("Failed to load climate_map.jpg.");
    };
}

function getClimateAt(lat, lng) {
    if (!climateContext) return "Loading Map...";
    
    // 1. Convert Lat/Lng to Pixel Coordinates (Simple Equirectangular)
    // Map bounds: [0,0] is Bottom-Left, [1000, 2000] is Top-Right (per lines 8-9) or [0,0] to [3000, 6000] pixel space?
    // In `app.js` line 8: `var bounds = [[0,0], [1000,2000]];`
    // Image is 6000x3000.
    // So Lat (0-1000) maps to Height (3000-0) ... Wait, Leaflet coordinates are Y, X.
    // [0,0] in Leaflet usually Bottom-Left?
    // Let's assume standard image overlay behavior:
    // Image Bottom-Left is (0,0) in Leaflet. Image Top-Right is (1000, 2000).
    // Canvas Top-Left (0,0) corresponds to Leaflet (1000, 0) because Canvas Y goes down.
    
    // Normalize Height (Y)
    // Leaflet Y: 0 to 1000. Canvas Y: 3000 to 0.
    // CanvasY = (1 - (Lat / 1000)) * 3000
    var yPct = 1 - (lat / 1000);
    var pixelY = Math.floor(yPct * mapHeight);
    
    // Normalize Width (X)
    // Leaflet X: 0 to 2000. Canvas X: 0 to 6000.
    // CanvasX = (Lng / 2000) * 6000
    var xPct = lng / 2000;
    var pixelX = Math.floor(xPct * mapWidth);
    
    // Bounds Check
    if (pixelX < 0 || pixelX >= mapWidth || pixelY < 0 || pixelY >= mapHeight) return "Out of Bounds";
    
    // 2. Sample Pixel
    var p = climateContext.getImageData(pixelX, pixelY, 1, 1).data; // [R, G, B, A]
    
    // 3. Find Closest Match (Euclidean Distance)
    var minDist = Infinity;
    var bestMatch = "Unknown";
    
    colorToClimate.forEach(c => {
        var dist = Math.sqrt(
            Math.pow(p[0] - c.color[0], 2) +
            Math.pow(p[1] - c.color[1], 2) +
            Math.pow(p[2] - c.color[2], 2)
        );
        if (dist < minDist) {
            minDist = dist;
            bestMatch = c.name;
        }
    });

    console.log(`Sampled [${p[0]},${p[1]},${p[2]}] at ${Math.round(lat)},${Math.round(lng)} -> ${bestMatch}`);
    return bestMatch; // + ` (${Math.round(minDist)})`;
}

function setDropdowns(cont, count) {
    document.getElementById('edit-continent').value = cont;
    document.getElementById('edit-continent').onchange(); // trigger update
    document.getElementById('edit-country').value = count;
}

// --- UI Logic: FAB Buttons ---
function setupEventListeners() {
    // Search
    document.getElementById('search-input').addEventListener('input', handleSearch);
    document.getElementById('menu-btn').addEventListener('click', () => {
        // Toggle Sidebar state? Or Open Menu?
        var sidebar = document.getElementById('sidebar');
        if (sidebar.classList.contains('open')) closeSidebar(); else openSidebar();
    });

    // FABs
    document.getElementById('fab-reset').onclick = () => {
        map.setView([500, 1000], -0.5);
    };

    document.getElementById('fab-wiki').onclick = () => {
        window.open('wiki/index.html', '_blank');
    };
    
    document.getElementById('fab-move').onclick = function() {
        moveMode = !moveMode;
        this.classList.toggle('active', moveMode);
        document.getElementById('map').style.cursor = moveMode ? "all-scroll" : "";
        
        // Toggle Draggable on all markers
        Object.values(layers).forEach(layer => {
            layer.eachLayer(marker => {
                 if (marker.dragging) {
                     moveMode ? marker.dragging.enable() : marker.dragging.disable();
                 }
            });
        });
    };

    document.getElementById('fab-add').onclick = function() {
        addMode = !addMode;
        this.classList.toggle('active', addMode);
        document.getElementById('map').style.cursor = addMode ? "crosshair" : "";
        if (!addMode && tempMarker) { map.removeLayer(tempMarker); tempMarker = null; }
    };
    
    // Sidebar Actions
    document.getElementById('btn-back-details').onclick = () => {
        // If we were editing existing city, go back to details. If adding new, close.
        if (currentCity) openSidebarDetails(currentCity.city, currentCity.continentName, currentCity.countryName);
        else closeSidebar();
    };
    document.getElementById('btn-cancel-edit').onclick = document.getElementById('btn-back-details').onclick;

    document.getElementById('btn-save-data').onclick = saveCityData;
    
    // Map Click (Add Mode or Close Sidebar)
    map.on('click', function(e) {
        if (addMode) {
            var coords = [parseFloat(e.latlng.lat.toFixed(1)), parseFloat(e.latlng.lng.toFixed(1))];
            
            if (tempMarker) map.removeLayer(tempMarker);
            tempMarker = L.marker(coords).addTo(map);
            
            if (tempMarker) map.removeLayer(tempMarker);
            tempMarker = L.marker(coords).addTo(map);
            
            // 1. Open Sidebar FIRST (resets form to defaults)
            openSidebarEdit(null); // Open in Add Mode
            
            // 2. Auto-Detect Data (with safety)
            try {
                var climate = getClimateAt(coords[0], coords[1]);
                var political = getPoliticalAt(coords[0], coords[1]);
                var alt = getAltitudeAt(coords[0], coords[1]);
    
                // 3. Populate Form with Detected Data (Overwriting defaults)
                document.getElementById('edit-climate').value = climate;
                document.getElementById('edit-altitude').value = alt;
                // Only try to set dropdowns if we have valid data
                if (political.continent !== "Unknown") {
                    setDropdowns(political.continent, political.country);
                }
            } catch (err) {
                console.error("Auto-Detect Failed:", err);
            }
            
            // 4. Always set Coords (Critical)
            document.getElementById('edit-coords').value = coords.join(', ');
            document.getElementById('edit-coords').value = coords.join(', ');
            
        } else {
            // If click on empty space, close sidebar
            // (Leaflet propagates click to map even if marker clicked, need check)
            // But marker click handler runs first. We can check target? 
            // Simplest: Marker click has L.DomEvent.stopPropagation if needed, 
            // but here we just rely on order. 
            // Actually, best to close sidebar ONLY if not clicking a marker.
            // But marker click is separate event.
        }
    });
}

function handleSearch(e) {
    var term = e.target.value.toLowerCase();
    var resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = '';
    
    if (term.length < 2) { resultsDiv.style.display = 'none'; return; }
    
    var matches = [];
    worldData.continents.forEach(cont => {
        cont.countries.forEach(count => {
            count.cities.forEach(city => {
                if (city.name.toLowerCase().includes(term)) {
                    matches.push({ city, cont, count });
                }
            });
        });
    });

    if (matches.length > 0) {
        resultsDiv.style.display = 'block';
        matches.slice(0, 5).forEach(m => {
            var div = document.createElement('div');
            div.className = 'search-result-item';
            div.innerText = `${m.city.name} (${m.count.name})`;
            div.onclick = () => {
                map.setView(m.city.coords, 1); // Zoom to city
                openSidebarDetails(m.city, m.cont.name, m.count.name);
                resultsDiv.style.display = 'none';
                document.getElementById('search-input').value = m.city.name;
            };
            resultsDiv.appendChild(div);
        });
    } else {
        resultsDiv.style.display = 'none';
    }
}

function saveCityData() {
    var name = document.getElementById('edit-name').value;
    var type = document.getElementById('edit-type').value;
    var continentName = document.getElementById('edit-continent').value;
    var countryName = document.getElementById('edit-country').value;
    var desc = document.getElementById('edit-desc').value;
    var pop = document.getElementById('edit-pop').value;
    var climate = document.getElementById('edit-climate').value;
    var alt = document.getElementById('edit-altitude').value; 
    var coordsStr = document.getElementById('edit-coords').value;
    
    if (!name || !coordsStr) { alert("Name and Coordinates required."); return; }
    
    var coords = coordsStr.split(',').map(Number);
    
    // Logic: If 'edit-country' is dropdown, use value. If readonly, use value.
    // Ensure we are sending data that server expects structure for.
    
    var cityData = {
        id: currentCity ? currentCity.city.id : Date.now().toString(), // Simple ID gen
        name: name,
        type: type,
        coords: coords,
        population: pop,
        climate: climate,
        desc: desc,
        altitude: alt 
    };

    var method = currentCity ? 'PUT' : 'POST'; // Correct Logic: existing city = PUT
    
    fetch('/api/cities', {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ continentName, countryName, city: cityData }) // Send correct object
    }).then(async res => {
        if (res.ok) {
            // Success
            loadMarkers();
            if (addMode) { 
                addMode = false; 
                document.getElementById('fab-add').classList.remove('active');
                if (tempMarker) { map.removeLayer(tempMarker); tempMarker = null; }
                document.getElementById('map').style.cursor = "";
            }
            closeSidebar();
            // console.log("Saved successfully");
        } else {
            // Error
            var txt = await res.text();
            alert("Save Failed: " + txt);
            console.error("Save Failed:", txt);
        }
    }).catch(err => {
        alert("Network Error: " + err);
        console.error("Network Error:", err);
    });
}

function updateCityOnServer(continentName, countryName, city) {
    fetch('/api/cities', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ continentName, countryName, city })
    }).then(res => {
        if (res.ok) console.log(`Updated ${city.name}`);
    });
}

function populateHierarchy() {
    var contSelect = document.getElementById('edit-continent');
    var countSelect = document.getElementById('edit-country');
    contSelect.innerHTML = '';
    
    worldData.continents.forEach(c => {
        var opt = document.createElement('option');
        opt.value = c.name; opt.innerText = c.name;
        contSelect.appendChild(opt);
    });

    const updateCountries = () => {
        countSelect.innerHTML = '';
        var continent = worldData.continents.find(c => c.name === contSelect.value);
        if (continent) {
            continent.countries.forEach(ct => {
                var opt = document.createElement('option');
                opt.value = ct.name; opt.innerText = ct.name;
                countSelect.appendChild(opt);
            });
        }
    };
    contSelect.onchange = updateCountries;
    updateCountries();
}

// Grid & Zoom logic (Keep from previous)
function drawGrid() {
    gridLayer.clearLayers();
    var step = 100;
    var gridStyle = { color: 'rgba(50,50,50,0.1)', weight: 1, interactive: false }; // Darker grid for white aesthetics
    for (var y = 0; y <= 1000; y += step) L.polyline([[y, 0], [y, 2000]], gridStyle).addTo(gridLayer);
    for (var x = 0; x <= 2000; x += step) L.polyline([[0, x], [1000, x]], gridStyle).addTo(gridLayer);
}

function updateZoomClasses() {
    var z = map.getZoom();
    var container = map.getContainer();
    container.classList.remove('zoom-planet', 'zoom-region', 'zoom-local');
    if (z <= -1) container.classList.add('zoom-planet');
    else if (z > -1 && z <= 0.5) container.classList.add('zoom-region');
    else container.classList.add('zoom-local');
}
map.on('zoomend', updateZoomClasses);
updateZoomClasses();

// --- Scale Control ---
L.Control.ScaleCustom = L.Control.extend({
    onAdd: function(map) {
        var el = L.DomUtil.create('div', 'leaflet-control-scale custom-scale');
        el.style.cssText = 'background:rgba(255,255,255,0.8); padding:2px 5px; border:1px solid #999; border-top:none; font-size:10px; color:#333; transition:width 0.2s; white-space:nowrap; text-align:center;box-shadow:0 1px 2px rgba(0,0,0,0.2);';
        el.innerHTML = '<div class="scale-label"></div>';
        return el;
    },
    onRemove: function(map) {}
});
var scaleControl = new L.Control.ScaleCustom({ position: 'bottomright' });
scaleControl.addTo(map);

function updateScale() {
    var el = document.querySelector('.custom-scale');
    if (!el) return;
    // 100 units = 2000 km logic
    var p1 = map.project([0,0], map.getZoom());
    var p2 = map.project([0,100], map.getZoom());
    var pxPer100Units = p2.x - p1.x;
    var kmPer100Units = 2000; 
    var pxPerKm = pxPer100Units / kmPer100Units;
    var targetPx = 150; 
    var maxKm = targetPx / pxPerKm;
    var rounding = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10];
    var finalKm = 10;
    for (var i = 0; i < rounding.length; i++) { if (maxKm >= rounding[i]) { finalKm = rounding[i]; break; } }
    var finalPx = finalKm * pxPerKm;
    el.style.width = finalPx + 'px';
    el.querySelector('.scale-label').innerText = finalKm + " km";
}
map.on('zoomend moveend', updateScale);
setTimeout(updateScale, 500);

// Initialize
// Initialize
function init() {
    loadMarkers();
    initClimateMap();
    initPoliticalMap(); // New
    initAltitudeMap();  // New
    drawGrid();
    setupEventListeners();
    
    // Default View: Political Composite
    politicalComposite.addTo(map);
    Object.values(layers).forEach(l => l.addTo(map));
    gridLayer.addTo(map);
    map.fitBounds(bounds);
    map.setZoom(-0.5);

    // Layer Control (Top Right, Collapsed)
    L.control.layers({
        "🗺️ Political": politicalComposite, 
        "🛰️ Satellite": satLayer, 
        "🏔️ Altitude": altLayer
    }, {
        "🏛️ Capitals": layers.capital,
        "🏙️ Metropolises": layers.metropolis, 
        "🏡 Settlements": layers.settlement, 
        "🏕️ Villages": layers.village, 
        "🔬 Special": layers.special,
        "🌐 Grid": gridLayer,
        "🚩 Frontiers": frontiersOverlay
    }, { collapsed: true }).addTo(map);
}

init();

// --- Political & Altitude Detection ---
var politicalContext = null;
var politicalLookup = null;
var altitudeContext = null;

function initPoliticalMap() {
    // Load Lookup JSON
    fetch('/data/political_lookup.json')
        .then(res => res.json())
        .then(data => { politicalLookup = data; });

    // Load Mask Image
    var canvas = document.getElementById('political-canvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    var img = new Image();
    img.src = '/data/political_mask.png';
    img.onload = function() {
        canvas.width = mapWidth;
        canvas.height = mapHeight;
        ctx.drawImage(img, 0, 0, mapWidth, mapHeight);
        politicalContext = ctx;
        console.log("Political Mask Loaded.");
    };
}

function initAltitudeMap() {
    var canvas = document.getElementById('altitude-canvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    var img = new Image();
    img.src = '/data/altitude_hifi.png';
    img.onload = function() {
        canvas.width = mapWidth;
        canvas.height = mapHeight;
        ctx.drawImage(img, 0, 0, mapWidth, mapHeight);
        altitudeContext = ctx;
        console.log("Altitude Map Loaded.");
    };
}

function getPoliticalAt(lat, lng) {
    if (!politicalContext || !politicalLookup) return { country: "Unknown", continent: "Unknown" };
    
    var xy = getPixelFromLatLng(lat, lng);
    if (!xy) return { country: "Out of Bounds", continent: "Out of Bounds" };

    var p = politicalContext.getImageData(xy.x, xy.y, 1, 1).data;
    var key = `${p[0]},${p[1]},${p[2]}`;
    console.log(`Political Sample: [${xy.x},${xy.y}] -> RGB(${key})`); // Debug
    
    return politicalLookup[key] || { country: "Wilderness/Ocean", continent: "Unknown" };
}

function getAltitudeAt(lat, lng) {
    if (!altitudeContext) return "Unknown";

    var xy = getPixelFromLatLng(lat, lng);
    if (!xy) return "0m";

    var p = altitudeContext.getImageData(xy.x, xy.y, 1, 1).data;
    // Hi-Fi PNG is linear: 0 = -10,000m, 255 = +10,000m
    var val = p[0]; 
    console.log(`Altitude Sample: [${xy.x},${xy.y}] -> Val(${val})`);
    var meters = Math.round((val / 255) * 20000 - 10000); 
    return `${meters}m`;
}

// Reuse logic from getClimateAt to avoid duplication
function getPixelFromLatLng(lat, lng) {
    var yPct = 1 - (lat / 1000);
    var pixelY = Math.floor(yPct * mapHeight);
    var xPct = lng / 2000;
    var pixelX = Math.floor(xPct * mapWidth);
    
    if (pixelX < 0 || pixelX >= mapWidth || pixelY < 0 || pixelY >= mapHeight) return null;
    return { x: pixelX, y: pixelY };
}
