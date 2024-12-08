"""Product search functionality using OpenAI API"""
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_product_description(interests: List[str], age: int, budget: float) -> str:
    """Generate a detailed product search prompt based on user interests and preferences"""
    prompt = f"""You are a gift recommendation expert. Given the following information about a person:
    - Age: {age}
    - Interests: {', '.join(interests)}
    - Budget: ${budget}
    
    Please suggest 4 specific gift ideas. For each gift, provide:
    1. Product name
    2. Price (within budget)
    3. Brief description
    4. Why it matches their interests
    5. A specific Amazon or Etsy product link
    
    Format as JSON array with fields: name, price, description, match_reason, amazon_link, etsy_link
    Keep descriptions concise and engaging."""
    
    return prompt

def search_products(interests: List[str], age: int, budget: float) -> List[Dict[str, Any]]:
    """Search for products using OpenAI API"""
    try:
        # Generate the prompt
        prompt = generate_product_description(interests, age, budget)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a gift recommendation expert who provides specific, purchasable product suggestions with real links."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            response_format={ "type": "json_object" }
        )
        
        # Parse the response
        recommendations = response.choices[0].message.content
        
        # Convert string to JSON if needed
        if isinstance(recommendations, str):
            import json
            recommendations = json.loads(recommendations)
        
        # Ensure we have the 'recommendations' key
        if 'recommendations' not in recommendations:
            recommendations = {'recommendations': recommendations}
            
        return recommendations['recommendations']
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        # Fallback to a default recommendation if API fails
        return [{
            "name": "Amazon Gift Card",
            "price": float(budget),
            "description": "A versatile gift card that lets them choose their perfect gift.",
            "match_reason": "Provides flexibility to choose based on personal interests",
            "amazon_link": "https://www.amazon.com/gift-cards",
            "etsy_link": None
        }]
