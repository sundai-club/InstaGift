from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI()  # This will automatically use the OPENAI_API_KEY from environment

def encode_image(image_file):
    """Convert image to base64 string"""
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_instagram_image(image_path: str) -> list:
    """
    Analyze an Instagram grid image to extract interests and preferences using OpenAI's vision model.
    """
    try:
        # Open and encode the image
        with open(image_path, 'rb') as image_file:
            base64_image = encode_image(image_file)

        # Create the message for OpenAI's vision model
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this Instagram grid image and identify the person's interests, hobbies, and preferences. List them as keywords."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        # Extract interests from the response
        interests_text = response.choices[0].message.content
        interests = [interest.strip() for interest in interests_text.split(',')]
        
        return interests[:10]  # Return top 10 interests

    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return ["photography", "travel", "food", "fashion", "technology"]  # Fallback interests
