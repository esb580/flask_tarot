from flask import Flask, jsonify
import random
import json
import copy

app = Flask(__name__)

# Load the tarot deck from pack.json
with open('pack.json', 'r') as f:
    tarot_deck = json.load(f)["pack"]  # Access the list inside the dictionary


# Shuffle the deck
def shuffle_deck():
    shuffled_deck = copy.deepcopy(tarot_deck)
    random.shuffle(shuffled_deck)
    return shuffled_deck


# Select cards from the shuffled deck
def select_cards(deck, num_cards):
    # Ensure num_cards is an integer
    if not isinstance(num_cards, int):
        raise ValueError("num_cards must be an integer")

    print(num_cards)
    print(len(deck))

    # Ensure num_cards is not greater than the length of the deck and is not negative
    if num_cards > len(deck) or num_cards < 0:
        raise ValueError("num_cards must be less than or equal to the length of the deck and must not be negative")
    selected_cards = random.sample(deck, num_cards)
    base_url = "http://<your-host-ip>:8080/"
    for card in selected_cards:
        orientation = "upright" if random.randint(0, 1) == 0 else "reversed"
        card["orientation"] = orientation.capitalize()
        card["image_url"] = "/img/" + orientation + "/" + card["card_image"]

        if orientation == "upright":
            card.pop("card_meaning_reversed", None)
            card.pop("card_description_reversed", None)
        else:  # orientation is "reversed"
            card.pop("card_meaning_upright", None)
            card.pop("card_description_upright", None)

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
