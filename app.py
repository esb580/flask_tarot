from flask import Flask, jsonify
import random
import json

app = Flask(__name__)

# Load the tarot deck from pack.json
with open('pack.json', 'r') as f:
    tarot_deck = json.load(f)

# Shuffle the deck
def shuffle_deck():
    shuffled_deck = tarot_deck.copy()
    random.shuffle(shuffled_deck)
    return shuffled_deck

# Select cards from the shuffled deck
def select_cards(deck, num_cards):
    selected_cards = random.sample(deck, num_cards)
    base_url = "http://<your-host-ip>:8080/img/"
    for card in selected_cards:
        card["orientation"] = "Upright" if random.randint(0, 1) == 0 else "Reversed"
        card["image_url"] = base_url + card["card_image"]
        card.pop("card_meaning_upright", None)
        card.pop("card_meaning_reversed", None)
        card.pop("card_description_upright", None)
        card.pop("card_description_reversed", None)
        card.pop("card_image", None)
    return selected_cards

@app.route('/tarot/3card', methods=['GET'])
def get_3card_reading():
    shuffled_deck = shuffle_deck()
    selected_cards = select_cards(shuffled_deck, 3)
    return jsonify(selected_cards)

@app.route('/tarot/5card', methods=['GET'])
def get_5card_reading():
    shuffled_deck = shuffle_deck()
    selected_cards = select_cards(shuffled_deck, 5)
    return jsonify(selected_cards)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
