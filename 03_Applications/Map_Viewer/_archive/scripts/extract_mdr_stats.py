import struct
import os
import numpy as np

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MDR_FILE = os.path.join(BASE_DIR, '01_Design_Sources', 'Kaelia Equirectangular.mdr')

# MDR Specs
HEADER_SIZE = 1024
WIDTH = 8192
HEIGHT = 4096

def main():
    if not os.path.exists(MDR_FILE):
        print(f"MDR File not found: {MDR_FILE}")
        return

    print(f"Analyzing {MDR_FILE}...")
    file_size = os.path.getsize(MDR_FILE)
    print(f"File size: {file_size / (1024*1024):.2f} MB")

    with open(MDR_FILE, 'rb') as f:
        f.seek(HEADER_SIZE)
        # Read the whole data as floats (32-bit little endian)
        raw_data = f.read()
        elevations = np.frombuffer(raw_data, dtype='<f4')
        
        # Reshape to 2D
        elevations = elevations.reshape((HEIGHT, WIDTH))
        
        # Statistics
        min_elev = np.min(elevations)
        max_elev = np.max(elevations)
        avg_elev = np.mean(elevations)
        
        # Land vs Water (assuming 0m is sea level)
        land_pixels = np.sum(elevations > 0)
        total_pixels = WIDTH * HEIGHT
        land_pct = (land_pixels / total_pixels) * 100
        water_pct = 100 - land_pct
        
        # Deepest and highest points
        y_max, x_max = np.unravel_index(np.argmax(elevations), elevations.shape)
        y_min, x_min = np.unravel_index(np.argmin(elevations), elevations.shape)
        
        # Convert pixel to pseudo-coordinates (simple map projection)
        def pix_to_coords(px, py):
            lat = 1000.0 * (1.0 - (py / HEIGHT))
            lng = 2000.0 * (px / WIDTH)
            return lat, lng

        max_lat, max_lng = pix_to_coords(x_max, y_max)
        min_lat, min_lng = pix_to_coords(x_min, y_min)

        print("\n--- MDR Terrain Statistics ---")
        print(f"Dimensions: {WIDTH}x{HEIGHT} pixels")
        print(f"Total Points: {total_pixels:,}")
        print(f"Elevation Range: {min_elev:.2f}m to {max_elev:.2f}m")
        print(f"Average Elevation: {avg_elev:.2f}m")
        print(f"Land Area estimation: {land_pct:.2f}%")
        print(f"Water Area estimation: {water_pct:.2f}%")
        print(f"\nHighest Point: {max_elev:.2f}m at pixel ({x_max}, {y_max}) -> Approx Coords (Lat: {max_lat:.1f}, Lng: {max_lng:.1f})")
        print(f"Lowest Point: {min_elev:.2f}m at pixel ({x_min}, {y_min}) -> Approx Coords (Lat: {min_lat:.1f}, Lng: {min_lng:.1f})")

if __name__ == "__main__":
    main()
