import os
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, Gio, GObject

def export_layers_v3_duplicate():
    # Setup Output
    base_path = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\02_Visual_Assets\1.0_Planet_Scale\Cartography"
    output_dir = os.path.join(base_path, "Exported_Layers")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get Active Image
    images = Gimp.get_images()
    if not images:
        print("No image found.")
        return

    # Find Source Image
    source_img = None
    for img in images:
        if "Kaelia" in img.get_name() or "Frontiers" in img.get_name():
            source_img = img
            break
    if not source_img:
        print("Could not find 'Kaelia' image. Using first available.")
        source_img = images[0]

    print(f"Exporting layers from '{source_img.get_name()}'...")

    # STRATEGY: Duplicate the WHOLE image to avoid messing with user's open file.
    # Then hide all layers, and reveal one by one for export.
    print("Duplicating image for safe export...")
    work_img = source_img.duplicate()

    # Get all layers
    layers = work_img.get_layers()

    # Disable all visibility first
    for layer in layers:
        layer.set_visible(False)

    for layer in layers:
        name = layer.get_name().strip()
        filename = os.path.join(output_dir, name + ".png")
        file = Gio.File.new_for_path(filename)
        
        print(f"Exporting: {name}")

        # Show this layer
        layer.set_visible(True)

        # Save the whole image (which now only shows this layer)
        # file_save saves the visible projection
        try:
            # Try 3-arg save first
            Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, work_img, file)
        except TypeError:
            try:
                # Try 4-arg save with None
                Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, work_img, [layer], file)
            except Exception as e:
                # Try specific detailed save
                try: 
                     Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, work_img, file, None)
                except Exception as e2:
                    print(f"Failed to save {name}: {e2}")

        # Hide again for next loop
        layer.set_visible(False)

    # Cleanup: Delete the duplicate image
    work_img.delete()

    print("--- Export Complete! ---")

export_layers_v3_duplicate()
