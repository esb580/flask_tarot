"""
flask_tarot_gen.py

Description: This file contains the logic for generating tarot card readings using the Google Generative AI model.
It includes a function for getting the interpretation of selected cards based on the spread type.

Author: esb580
Created: 4/29/2024
Last Modified: 4/29/2024

"""
import os
import google.generativeai as genai

# Load the environment variables from the .env file
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
print("Google API Key: " + os.getenv('GOOGLE_API_KEY'))

# Configure the API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.0-pro-latest')
# response = model.generate_content("The opposite of hot is")


def get_interpretation(cards, spread):
    if spread == "3card":
        the_spread = "a three-card"
    elif spread == "5card":
        the_spread = "a five-card"
    else:
        raise ValueError("spread must be either '3card' or '5card")

    # Ensure cards is a list
    if not isinstance(cards, list):
        raise ValueError("cards must be a list")

    # Ensure spread is a string
    if not isinstance(spread, str):
        raise ValueError("spread must be a string")

    # Ensure cards is not empty
    if len(cards) == 0:
        raise ValueError("cards must not be empty")

    # Get the card names with numbers
    card_names = [f"{i+1}. {card['card_name']} - {card['orientation']}" for i, card in enumerate(cards)]

    # Generate the content
    content = "Using " + the_spread + " tarot spread with standard conventions, please give a reading: " + ", ".join(card_names)
    response = model.generate_content(content)
    return response.text



