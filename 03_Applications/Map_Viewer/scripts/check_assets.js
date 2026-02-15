const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '../data/master_world_data.json');
const rootDir = path.join(__dirname, '..'); 
const reportPath = path.join(__dirname, 'asset_report_utf8.txt');

try {
    const rawData = fs.readFileSync(dataPath, 'utf8');
    const worldData = JSON.parse(rawData);
    
    let report = "--- Checking Asset Existence ---\n";
    let missingCount = 0;
    let checkedCount = 0;
    
    worldData.continents.forEach(continent => {
        continent.countries.forEach(country => {
            if (!country.cities) return;
            
            country.cities.forEach(city => {
                checkedCount++;
                if (city.image) {
                    const relativePath = city.image.replace(/\//g, path.sep); 
                    const fullPath = path.join(rootDir, relativePath);
                    
                    if (!fs.existsSync(fullPath)) {
                        report += `[MISSING] ${city.name} (${city.id}): ${city.image}\n`;
                        missingCount++;
                    }
                } else {
                     report += `[NO_REF] ${city.name} (${city.id}) has no image property.\n`;
                }
            });
        });
    });
    
    report += "--------------------------------\n";
    report += `Checked: ${checkedCount}\n`;
    report += `Missing: ${missingCount}\n`;
    
    fs.writeFileSync(reportPath, report, 'utf8');
    console.log("Report written to " + reportPath);
    
} catch (err) {
    console.error("Error:", err);
}
