from PIL import Image
import os

def composite_layers():
    # Paths
    base_path = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\02_Visual_Assets\1.0_Planet_Scale\Cartography\Exported_Layers"
    output_path = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\03_Applications\Map_Viewer\data\frontiers_overlay.png"

    # Files to exclude
    exclude = ["Background.png", "Planeta 1 Equirectangular Sphere Map B&W.png", "Planeta 1 Equirectangular Sphere Map Altitude.png", "Copia de Betereko.png"]
    
    # Get list of files
    files = [f for f in os.listdir(base_path) if f.endswith(".png") and f not in exclude]
    
    if not files:
        print("No files to process.")
        return

    print(f"Found {len(files)} country layers.")

    # Create base canvas (Transparent)
    # We'll open the first image to get dimensions
    first_img = Image.open(os.path.join(base_path, files[0]))
    width, height = first_img.size
    composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Composite
    for filename in files:
        print(f"Adding: {filename}")
        img_path = os.path.join(base_path, filename)
        layer = Image.open(img_path).convert("RGBA")
        
        # Alpha composite
        composite.alpha_composite(layer)

    # Save
    print(f"Saving to {output_path}...")
    composite.save(output_path, "PNG")
    print("Done!")

if __name__ == "__main__":
    composite_layers()
