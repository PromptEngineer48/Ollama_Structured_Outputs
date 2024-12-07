from ollama import chat
from pydantic import BaseModel, ValidationError
from typing import List, Literal, Optional
import json  # To parse JSON responses

class Object(BaseModel):
    name: str = "Unknown"
    confidence: float = 0.0
    attributes: str = "None"

class ImageDescription(BaseModel):
    summary: Optional[str] = "No summary available"
    objects: List[Object] = []
    scene: Optional[str] = "Unknown"
    colors: List[str] = []
    time_of_day: Literal['Morning', 'Afternoon', 'Evening', 'Night'] = "Unknown"
    setting: Literal['Indoor', 'Outdoor', 'Unknown'] = "Unknown"
    text_content: Optional[str] = None

path = 'image.jpg'

response = chat(
    model='llama3.2-vision',
    format="json",  # Pass 'json' for structured JSON output
    messages=[
        {
            'role': 'user',
            'content': 'Analyze this image and describe what you see, including any objects, the scene, colors and any text you can detect.',
            'images': [path],
        },
    ],
    options={'temperature': 0},  # Set temperature to 0 for more deterministic output
)

try:
    # Parse the response content as JSON
    response_data = json.loads(response.message.content)
    print(response_data)

    # Fill in missing fields with defaults
    image_description = ImageDescription.model_validate(response_data)
    print(image_description)

except json.JSONDecodeError:
    print("Error decoding the response content as JSON.")
    
except ValidationError as e:
    print("Validation error:", e.json())
