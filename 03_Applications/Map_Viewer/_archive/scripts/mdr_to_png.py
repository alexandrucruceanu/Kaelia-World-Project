import struct
import os
from PIL import Image
import numpy as np

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MDR_FILE = os.path.join(BASE_DIR, '01_Design_Sources', 'Kaelia Equirectangular.mdr')
OUTPUT_FILE = os.path.join(BASE_DIR, '03_Applications', 'Map_Viewer', 'data', 'altitude_hifi.png')

# MDR Specs
HEADER_SIZE = 1024
WIDTH = 8192
HEIGHT = 4096

def main():
    if not os.path.exists(MDR_FILE):
        print(f"MDR File not found: {MDR_FILE}")
        return

    with open(MDR_FILE, 'rb') as f:
        f.seek(HEADER_SIZE)
        # Read the whole data as floats
        raw_data = f.read()
        elevations = np.frombuffer(raw_data, dtype='<f4').reshape((HEIGHT, WIDTH))
        
        # Mapping: -10000 to +10000 -> 0 to 255
        # 127 is approx 0m
        scaled = ((elevations + 10000.0) / 20000.0 * 255.0)
        scaled = np.clip(scaled, 0, 255).astype(np.uint8)
        
        img = Image.fromarray(scaled, mode='L')
        # Resize to 6000x3000 to match current app expectations (optional but safer)
        img = img.resize((6000, 3000), Image.Resampling.LANCZOS)
        img.save(OUTPUT_FILE)
        
        print(f"Saved hi-fi altitude map to {OUTPUT_FILE}")
        print(f"Precision: ~78m per gray level. Range: -10,000m to +10,000m")

if __name__ == "__main__":
    main()
