import openai
from pathlib import Path
from dotenv import load_dotenv
import os
import base64

# Load variables from .env
load_dotenv()

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def GPT_4o_response(image_bytes: bytes, prompt: str) -> str:
    # Encode image as base64
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=1024,
        temperature=0.2,
    )

    return response.choices[0].message["content"]
