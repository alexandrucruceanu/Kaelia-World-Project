import json
import os
import sys
import subprocess

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_SCRIPT = os.path.join(SCRIPT_DIR, "generate_assets_hybrid.py")
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "master_world_data.json")

def verify_generation():
    # 1. Read a city to get its stored prompt
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find a city with prompts
    target_city = None
    for continent in data.get('continents', []):
        for country in continent.get('countries', []):
            for city in country.get('cities', []):
                if 'prompts' in city:
                    target_city = city
                    break
            if target_city: break
        if target_city: break
    
    if not target_city:
        print("FAIL: No city found with stored prompts.")
        return

    print(f"Testing with city: {target_city['name']} (ID: {target_city['id']})")
    stored_prompt = target_city['prompts']['landscape_main']
    
    # 2. Run generator in construct-only mode
    # We expect it to return the STORED prompt, which we can identify by the specific camera angle change
    # "High-angle oblique view" vs "Top-down (Nadir)"
    
    cmd = [sys.executable, GEN_SCRIPT, "--id", target_city['id'], "--type", "landscape_main", "--construct-only"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"FAIL: Generator script failed: {result.stderr}")
        return

    try:
        output_json = json.loads(result.stdout)
        generated_prompt_str = output_json.get('prompt')
        generated_prompt = json.loads(generated_prompt_str)
        
        angle = generated_prompt.get('composition', {}).get('camera_angle', '')
        print(f"Camera Angle found: {angle}")
        
        if "High-angle oblique" in angle or "45-degree" in angle:
            print("SUCCESS: Generator used the stored oblique prompt.")
        elif "Top-down" in angle:
            print("FAIL: Generator used the algorithmic Zenithal prompt (Migration failed or Script ignoring JSON).")
        else:
            print("WARNING: Unknown angle. Manual check required.")
            
    except json.JSONDecodeError as e:
        print(f"FAIL: Could not decode JSON output: {e}")
        print(f"Raw Output: {result.stdout}")

if __name__ == "__main__":
    verify_generation()
