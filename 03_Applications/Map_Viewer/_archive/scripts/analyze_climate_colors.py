from PIL import Image
import collections

def analyze_colors():
    image_path = r"g:\Mi unidad\01_Alex\30_Tecnologia_y_Proyectos\World_Building_Project\03_Applications\Map_Viewer\data\climate_map.jpg"
    
    print(f"Analyzing: {image_path}")
    img = Image.open(image_path)
    # Resize for speed - we just want dominant colors
    img = img.resize((500, 250))
    # Convert to RGB (remove alpha if present)
    img = img.convert("RGB")
    
    pixels = list(img.getdata())
    
    # Count colors
    counter = collections.Counter(pixels)
    
    # Get top 20
    top_colors = counter.most_common(20)
    
    print("Top 20 Colors found:")
    for color, count in top_colors:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        print(f"Color: {hex_color} (RGB: {color}) - Count: {count}")

if __name__ == "__main__":
    analyze_colors()
