"""
app.py

Description: Enhanced version of the Tarot card reading web service with cryptographic randomness.
It includes routes for getting 3-card and 5-card readings.

Author: esb580
Created: 3/30/2025
Last Modified: 3/30/2025
"""

from flask import Flask, jsonify
from flask import render_template
import secrets
import json
import copy
import markdown
import os
import hashlib
import time
from flask_tarot_gen import get_interpretation

app = Flask(__name__)

# Load the tarot deck from pack.json
with open('pack.json', 'r') as f:
    tarot_deck = json.load(f)["pack"]

def get_entropy_seed():
    """Generate a random seed using multiple entropy sources"""
    entropy = str(os.urandom(16)) + \
              str(time.time_ns()) + \
              str(os.getpid()) + \
              str(secrets.token_bytes(16))
    return int(hashlib.sha256(entropy.encode()).hexdigest(), 16)

def shuffle_deck(spread="3card"):
    """Cryptographically secure deck shuffling"""
    if not isinstance(spread, str):
        raise ValueError("spread must be a string")

    if spread == "3card":
        deck = copy.deepcopy(tarot_deck[:22])
    elif spread == "5card":
        deck = copy.deepcopy(tarot_deck)
    else:
        raise ValueError("spread must be either '3card' or '5card'")

    # Fisher-Yates shuffle with secrets
    shuffled_deck = deck.copy()
    for i in range(len(shuffled_deck) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        shuffled_deck[i], shuffled_deck[j] = shuffled_deck[j], shuffled_deck[i]

    return shuffled_deck

def select_cards(deck, num_cards):
    """Select cards using cryptographically secure random numbers"""
    if not isinstance(num_cards, int):
        raise ValueError("num_cards must be an integer")

    if num_cards > len(deck) or num_cards < 0:
        raise ValueError("num_cards must be less than or equal to the length of the deck and must not be negative")

    print(f"The deck has {len(deck)} cards in it.")
    print(f"Drawing {num_cards} cards from the deck...")

    # Get system entropy
    system_entropy = get_entropy_seed()
    
    # Select cards
    selected_cards = []
    temp_deck = deck.copy()
    
    for _ in range(num_cards):
        index = secrets.randbelow(len(temp_deck))
        card = temp_deck.pop(index)
        
        # Use system entropy + secrets for orientation
        entropy_value = secrets.randbelow(system_entropy) % 2
        orientation = "upright" if entropy_value == 0 else "reversed"
        
        card["orientation"] = orientation
        card["image_url"] = f"/img/{orientation}/{card['card_image']}"

        if orientation == "upright":
            card.pop("card_meaning_reversed", None)
            card.pop("card_description_reversed", None)
        else:
            card.pop("card_meaning_upright", None)
            card.pop("card_description_upright", None)

        print(f"Selected card: {card['card_name']} - {orientation}")
        selected_cards.append(card)

    return selected_cards

@app.route('/tarot/api/3card', methods=['GET'])
def get_3card_reading():
    shuffled_deck = shuffle_deck('3card')
    selected_cards = select_cards(shuffled_deck, 3)
    return jsonify(selected_cards)

@app.route('/tarot/api/5card', methods=['GET'])
def get_5card_reading():
    shuffled_deck = shuffle_deck('5card')
    selected_cards = select_cards(shuffled_deck, 5)
    return jsonify(selected_cards)

@app.route('/tarot/reading/3card', methods=['GET'])
def get_3card_reading_web():
    shuffled_deck = shuffle_deck('3card')
    selected_cards = select_cards(shuffled_deck, 3)
    ai_reading = get_interpretation(selected_cards, "3card")
    html_reading = markdown.markdown(ai_reading)
    return render_template('3card_reading.html', reading=html_reading, cards=selected_cards)

@app.route('/tarot/reading/5card', methods=['GET'])
def get_5card_reading_web():
    shuffled_deck = shuffle_deck('5card')
    selected_cards = select_cards(shuffled_deck, 5)
    ai_reading = get_interpretation(selected_cards, "5card")
    html_reading = markdown.markdown(ai_reading)
    return render_template('5card_reading.html', reading=html_reading, cards=selected_cards)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/img/<orientation>/<path:filename>')
def get_image(orientation, filename):
    return app.send_static_file(f"img/{orientation}/{filename}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)