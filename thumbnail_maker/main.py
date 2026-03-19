import requests
import base64
import os

API_KEY = os.getenv("OPENAI_API_KEY")

url = "https://api.openai.com/v1/images/edits"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

files = [
    ("image[]", ("logo.png", open("resources/logo.png", "rb"), "image/png")),
    ("image[]", ("The_Turtleing.png", open("resources/The_Turtleing.png", "rb"), "image/png")),
]

data = {
    "model": "gpt-image-1.5",
    "prompt": """
Create a high-quality YouTube thumbnail (16:9).

Use the provided images:
- Place the clan badge in center
- Use the logo style to style your output

Add bold, large text below the banner:
"March CWL RECAP"

Add smaller text above:
"The Turtleing"

Style:
- Clash of Clans theme but do not alter the clan banner
- Fiery background (orange, yellow glow, explosions)
- High contrast
- Thick outlined text
- Clean, clickable YouTube thumbnail style

Make sure text is readable at small sizes.
""",
    "size": "1536x1024",   # closest to 16:9
    "quality": "high",
    "input_fidelity": "high"
}

response = requests.post(url, headers=headers, files=files, data=data)

# Handle response
result = response.json()

# Decode and save image
image_base64 = result["data"][0]["b64_json"]
image_bytes = base64.b64decode(image_base64)

with open("thumbnail.png", "wb") as f:
    f.write(image_bytes)

print("Thumbnail saved as thumbnail.png")