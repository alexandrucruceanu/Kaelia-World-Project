import cv2
import numpy as np
import os

"""
Advanced Frontier and Name Extraction Script
============================================
Extracted from Claude's recommendation and refined for the Kaelia Map Viewer.
This version uses 'Image Difference' to perfectly isolate labels and lines.
"""

def extract_frontiers_refined(labeled_path, clean_path, output_dir, thresh=15, dilation=1, soft_alpha=True):
    print(f"--- Refining Extraction (Threshold: {thresh}, Dilation: {dilation}) ---")
    
    img_labeled = cv2.imread(labeled_path)
    img_clean = cv2.imread(clean_path)
    
    if img_labeled is None or img_clean is None:
        return

    if img_labeled.shape != img_clean.shape:
        img_clean = cv2.resize(img_clean, (img_labeled.shape[1], img_labeled.shape[0]))

    # 1. Difference Mask
    diff = cv2.absdiff(img_labeled, img_clean)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # 2. Color Mask (Ensure we only target yellow)
    hsv = cv2.cvtColor(img_labeled, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 80, 80])
    upper_yellow = np.array([40, 255, 255])
    color_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 3. Combine Difference and Color
    _, diff_mask = cv2.threshold(diff_gray, thresh, 255, cv2.THRESH_BINARY)
    final_mask = cv2.bitwise_and(diff_mask, color_mask)

    # 4. Morphological Cleanup & Dilation
    kernel = np.ones((2, 2), np.uint8)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    if dilation > 0:
        final_mask = cv2.dilate(final_mask, kernel, iterations=dilation)

    # 5. Transparency Logic
    if soft_alpha:
        # Use a blurred version of the mask for smoother edges
        alpha = cv2.GaussianBlur(final_mask, (3, 3), 0)
    else:
        alpha = final_mask

    # Create a solid yellow canvas (BGR: 0, 255, 255 for standard yellow, or 0, 215, 255 for Gold)
    # Using specific Gold/Yellow for Kaelia: (0, 215, 255)
    yellow_canvas = np.zeros_like(img_labeled)
    yellow_canvas[:] = (0, 215, 255) # Gold/Yellow BGR

    # Mask the solid canvas with our alpha
    # We apply the mask to the solid color, so no blue/black artifacts from the original map remain.
    b, g, r = cv2.split(yellow_canvas)
    rgba = cv2.merge([b, g, r, alpha])

    # Save
    name = f"frontiers_refined_t{thresh}_d{dilation}.png"
    output_path = os.path.join(output_dir, name)
    cv2.imwrite(output_path, rgba)
    
    # Also update the main overlay
    if thresh == 15 and dilation == 1:
        cv2.imwrite(os.path.join(output_dir, "frontiers_overlay.png"), rgba)
    
    print(f"Saved: {name}")

if __name__ == "__main__":
    LABELED = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\02_Visual_Assets\1.0_Planet_Scale\Cartography\Kaelia Equirectangular Sphere Map Names & Frontiers.jpg"
    CLEAN = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\02_Visual_Assets\1.0_Planet_Scale\Cartography\Kaelia Equirectangular Sphere Map.jpg"
    OUTPUT_DIR = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\03_Applications\Map_Viewer\data"

    # Generate a few options for the user
    extract_frontiers_refined(LABELED, CLEAN, OUTPUT_DIR, thresh=10, dilation=1)
    extract_frontiers_refined(LABELED, CLEAN, OUTPUT_DIR, thresh=15, dilation=1) # Balanced
    extract_frontiers_refined(LABELED, CLEAN, OUTPUT_DIR, thresh=15, dilation=2) # Thicker

