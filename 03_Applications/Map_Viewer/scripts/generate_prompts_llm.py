import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env file
load_dotenv()

# Default to Gemini 3.0 Flash
MODEL_ID = "gemini-3-flash-preview"

SYSTEM_INSTRUCTION = """
You are an expert World-Building Artist and Prompt Engineer for a high-end fantasy/sci-fi project called 'Kaelia'.
Your task is to generate 5 distinct, high-quality image generation prompts based on the provided JSON data about a city.
The prompts must be returned in a strict JSON format.

Input Data will include:
- Name, Type, Biome, Population, Description, Lore, Visual Data Schema, Heraldry.

Output JSON Structure:
{
  "landscape_main": { ... },     // Aerial/Satellite view
  "landscape_seq1": { ... },     // Eye-level Street View
  "landscape_seq2": { ... },     // Photojournalistic/Gritty View
  "heraldry_flag": { ... },      // Flat Vector Flag
  "heraldry_arms": { ... }       // Flat Vector Coat of Arms
}

Each prompt object must follow the project's specific schema:
{
  "meta": { "image_type": "...", "aspect_ratio": "..." },
  "global_context": { "scene_description": "...", "lighting": "...", "atmosphere": "..." },
  "composition": { "camera_angle": "...", "focal_point": "..." },
  "objects": [ ... ]
}

Notes:
- Use the provided 'visual_data' as a strong style guide.
- 'landscape_main': 4:3 aspect ratio. High altitude, showing the city layout and biome integration.
- 'landscape_seq1': 4:3 aspect ratio. Street level, showing architecture and scale.
- 'landscape_seq2': 4:3 aspect ratio. Atmospheric, focusing on texture, daily life, or specific details.
- 'heraldry_flag': 3:2 aspect ratio. Flat vector, clean, 2D.
- 'heraldry_arms': 1:1 aspect ratio. Flat vector, shield shape, bold lines.
- Be creative but faithful to the provided lore and biome.
"""

def generate_prompts(api_key, city_data):
    if not api_key:
        return {"error": "API Key not found"}

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Generate strict JSON prompts for the following city:
        
        {json.dumps(city_data, indent=2)}
        """

        # Using simpler structure for generation request as per `generate_assets_hybrid.py` example
        # but adapting for text-only response (prompt generation)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json"
            )
        )
        
        # Clean up response (handle Markdown code blocks)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        return json.loads(text.strip())

    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Generate Kaelia city prompts using Gemini 2.0 Flash.")
    parser.add_argument("--city_json", help="JSON string of city data", required=True)
    args = parser.parse_args()

    # Get API Key from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Fallback to hardcoded key if env var missing (not ideal but safe for local dev if user has it set elsewhere)
        # Actually better to fail gracefully
        print(json.dumps({"error": "GEMINI_API_KEY environment variable not set"}))
        return

    try:
        city_data = json.loads(args.city_json)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON string provided"}))
        return

    result = generate_prompts(api_key, city_data)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
