"""
flask_tarot_gen_2_0.py

Description: This file contains the logic for generating tarot card readings using Google's Generative AI.
Uses google-genai library for improved performance and features.

Author: esb580
Created: 4/29/2024
Last Modified: 3/30/2025
"""
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Initialize the client
client = genai.Client(api_key=api_key)

def get_interpretation(cards, spread):
    """
    Get a tarot reading interpretation using Google's Generative AI.
    
    Args:
        cards (list): List of card dictionaries
        spread (str): Type of spread ('3card' or '5card')
    
    Returns:
        str: Generated interpretation text
    """
    if spread == "3card":
        the_spread = "a three-card"
    elif spread == "5card":
        the_spread = "a five-card"
    else:
        raise ValueError("spread must be either '3card' or '5card'")

    # Input validation
    if not isinstance(cards, list):
        raise ValueError("cards must be a list")
    if not cards:
        raise ValueError("cards must not be empty")
    if not isinstance(spread, str):
        raise ValueError("spread must be a string")

    # Format card names
    card_names = [
        f"{i+1}. {card['card_name']} - {card['orientation']}" 
        for i, card in enumerate(cards)
    ]

    # Prepare prompt
    content = (
        f"Using {the_spread} tarot spread with standard conventions, "
        f"please give a reading: {', '.join(card_names)}"
    )

    try:
        # Generate content with new API
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=content,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=1000,
            )
        )
        
        return response.text

    except Exception as e:
        raise RuntimeError(f"Failed to generate interpretation: {str(e)}")