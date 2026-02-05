import cv2
import numpy as np
import os

def extract_yellow(image_path, output_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}")
        return

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for yellow color in HSV
    # Use a wider range to catch anti-aliased edges and text
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    # Create mask
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Optional: Dilate slightly to bridge any gaps in the frontier lines
    kernel = np.ones((2,2), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Create an RGBA image
    # Extract only the yellow parts
    yellow_only = cv2.bitwise_and(img, img, mask=mask)
    
    # Add Alpha channel
    b, g, r = cv2.split(yellow_only)
    # The mask itself serves as the alpha channel
    rgba = cv2.merge([b, g, r, mask])

    # Save as transparent PNG
    cv2.imwrite(output_path, rgba)
    print(f"Successfully saved frontier overlay to {output_path}")

if __name__ == "__main__":
    input_file = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\02_Visual_Assets\1.0_Planet_Scale\Cartography\Kaelia Equirectangular Sphere Map Names & Frontiers.jpg"
    output_file = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\03_Applications\Map_Viewer\data\frontiers_overlay.png"
    
    # Ensure background data dir exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    extract_yellow(input_file, output_file)
