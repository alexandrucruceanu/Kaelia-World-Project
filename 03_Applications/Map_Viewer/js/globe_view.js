let is3D = false;
let globe = null;

function initGlobe() {
    if (globe) return;

    globe = Globe()
        (document.getElementById('globe-container'))
        .globeImageUrl('img/satellite.jpg')
        .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
        .pointRadius(d => {
            const config = (window.categoryConfig && window.categoryConfig[d.city.type]) || { radius: 5 };
            return config.radius / 10; // Scaled for globe
        })
        .pointColor(d => d.city.color || '#ea4335')
        .pointLabel(d => `
            <div style="background: rgba(0,0,0,0.8); color: white; padding: 5px 10px; border-radius: 4px; border: 1px solid #555;">
                <b style="font-size: 1.1em;">${d.name}</b><br/>
                <span style="color: #ccc; font-size: 0.9em;">${d.countryName}, ${d.continentName}</span>
            </div>
        `)
        .onPointClick(point => {
            if (typeof openSidebarDetails === 'function') {
                openSidebarDetails(point.city, point.continentName, point.countryName);
            }
        });

    globe.controls().autoRotate = true;
    globe.controls().autoRotateSpeed = 0.5;

    // Load data from existing worldData if available, otherwise fetch
    if (window.worldData && window.worldData.continents) {
        loadGlobeData(window.worldData);
    } else {
        fetch('/api/world')
            .then(res => res.json())
            .then(data => {
                window.worldData = data;
                loadGlobeData(data);
            });
    }

    window.addEventListener('resize', () => {
        globe.width(window.innerWidth);
        globe.height(window.innerHeight);
    });
}

function loadGlobeData(data) {
    const points = [];
    data.continents.forEach(continent => {
        continent.countries.forEach(country => {
            if (country.cities) {
                country.cities.forEach(city => {
                    if (city.coords && city.coords.length === 2) {
                        points.push({
                            lat: (city.coords[0] / 1000) * 180 - 90,
                            lng: (city.coords[1] / 2000) * 360 - 180,
                            name: city.name,
                            city: city,
                            continentName: continent.name,
                            countryName: country.name
                        });
                    }
                });
            }
        });
    });
    globe.pointsData(points);
}

function toggle3D() {
    is3D = !is3D;
    const mapEl = document.getElementById('map');
    const globeEl = document.getElementById('globe-container');
    const toggleBtn = document.getElementById('fab-view-toggle');

    if (is3D) {
        mapEl.style.display = 'none';
        globeEl.style.display = 'block';
        toggleBtn.innerText = '🗺️';
        toggleBtn.dataset.tooltip = 'Switch to 2D Map';
        initGlobe();
    } else {
        mapEl.style.display = 'block';
        globeEl.style.display = 'none';
        toggleBtn.innerText = '🌍';
        toggleBtn.dataset.tooltip = 'Switch to 3D Globe';
    }
}

document.getElementById('fab-view-toggle').addEventListener('click', toggle3D);
