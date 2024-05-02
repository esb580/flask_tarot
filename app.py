"""
app.py

Description: This file contains the main application logic for the Tarot card reading web service.
It includes routes for getting 3-card and 5-card readings.

Author: esb580
Created: 4/29/2024
Last Modified: 4/29/2024

"""
from flask import Flask, jsonify
from flask import render_template
import random
import json
import copy
from flask_tarot_gen import get_interpretation

app = Flask(__name__)

# Load the tarot deck from pack.json
with open('pack.json', 'r') as f:
    tarot_deck = json.load(f)["pack"]  # Access the list inside the dictionary


# Shuffle the deck
def shuffle_deck(spread="3card"):
    # Ensure spread is a string
    if not isinstance(spread, str):
        raise ValueError("spread must be a string")

    # Only take the first 22 cards if the is for 3card reading
    if spread == "3card":
        shuffled_deck = copy.deepcopy(tarot_deck[:22])
    # Take all 78 cards if the spread is for 5card reading
    elif spread == "5card":
        shuffled_deck = copy.deepcopy(tarot_deck)
    else:
        raise ValueError("spread must be either '3card' or '5card'")

    random.shuffle(shuffled_deck)
    return shuffled_deck


# Select cards from the shuffled deck
def select_cards(deck, num_cards):
    # Ensure num_cards is an integer
    if not isinstance(num_cards, int):
        raise ValueError("num_cards must be an integer")

    print("The deck has " + str(len(deck)) + " cards in it.")
    print("Drawing " + str(num_cards) + " cards from the deck...")

    # Ensure num_cards is not greater than the length of the deck and is not negative
    if num_cards > len(deck) or num_cards < 0:
        raise ValueError("num_cards must be less than or equal to the length of the deck and must not be negative")
    selected_cards = random.sample(deck, num_cards)
    # base_url = "http://<your-host-ip>:8080/"
    for card in selected_cards:
        orientation = "upright" if random.randint(0, 1) == 0 else "reversed"
        card["orientation"] = orientation
        card["image_url"] = "/img/" + orientation + "/" + card["card_image"]

        if orientation == "upright":
            card.pop("card_meaning_reversed", None)
            card.pop("card_description_reversed", None)
        else:  # orientation is "reversed"
            card.pop("card_meaning_upright", None)
            card.pop("card_description_upright", None)

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


@app.route('/tarot/reading/3card', methods=['GET'])  # This route is for the web page
def get_3card_reading_web():
    shuffled_deck = shuffle_deck('3card')
    selected_cards = select_cards(shuffled_deck, 3)
    print(selected_cards)
    ai_reading = get_interpretation(selected_cards, "3card")
    return render_template('3card_reading.html', reading=ai_reading, cards=selected_cards)


@app.route('/img/<orientation>/<path:filename>')
def get_image(orientation, filename):
    return app.send_static_file("img/" + orientation + "/" + filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
