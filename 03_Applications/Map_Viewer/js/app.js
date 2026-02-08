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
var frontiersOverlay = L.imageOverlay('data/frontiers_refined_t15_d1.png', bounds, { opacity: 1.0, interactive: false });
var politicalComposite = L.layerGroup([satLayer, frontiersOverlay]);

var worldData = {};
var currentCity = null; // Currently selected city
var moveMode = false;
var addMode = false;
var tempMarker = null; // Marker for adding new loc

// --- Initialization ---
function init() {
    loadMarkers();
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
        "�️ Capitals": layers.capital,
        "�🏙️ Metropolises": layers.metropolis, 
        "🏡 Settlements": layers.settlement, 
        "🏕️ Villages": layers.village, 
        "🔬 Special": layers.special,
        "🌐 Grid": gridLayer,
        "🚩 Frontiers": frontiersOverlay
    }, { collapsed: true }).addTo(map);
}

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
    document.getElementById('detail-region').innerText = `${countryName}, ${continentName}`;
    
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
        document.getElementById('edit-desc').value = city.desc;
        
        setDropdowns(continentName, countryName);
    } else {
        // Add Mode
        document.querySelector('.form-header h2').innerText = "Add Location";
        document.getElementById('edit-name').value = "";
        document.getElementById('edit-desc').value = "";
        document.getElementById('edit-pop').value = "";
        // Coords should be set by click map logic
    }
    
    openSidebar();
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
            
            document.getElementById('edit-coords').value = coords.join(', ');
            openSidebarEdit(null); // Open in Add Mode
            
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
    var population = document.getElementById('edit-pop').value;
    var coordsStr = document.getElementById('edit-coords').value;
    
    if (!name || !coordsStr) { alert("Name and Coordinates required."); return; }
    
    var coords = coordsStr.split(',').map(Number);
    
    var city = {
        id: currentCity ? currentCity.city.id : null, 
        name, type, coords, desc, population, color: "#ea4335"
    };

    var method = city.id ? 'PUT' : 'POST';
    
    fetch('/api/cities', {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ continentName, countryName, city })
    }).then(res => {
        if (res.ok) {
            // alert("Saved!");
            loadMarkers();
            if (currentCity) {
                // Determine new ID (if post, we don't know it without response parsing, 
                // but let's just reload markers and close for now or fetch new city)
                // Ideally API returns new city object.
            }
            if (addMode) { 
                addMode = false; 
                document.getElementById('fab-add').classList.remove('active');
                map.removeLayer(tempMarker);
                tempMarker = null;
                document.getElementById('map').style.cursor = "";
            }
            closeSidebar();
        }
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
init();
