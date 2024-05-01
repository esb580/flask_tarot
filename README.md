# Flask Tarot API

This is a Flask application that provides a Tarot card reading API and web interface. The application uses a JSON file to load a Tarot deck and provides two API endpoints and corresponding web pages for different types of readings.

## API Endpoints

### 3 Card Reading

**Endpoint:** `/tarot/reading/3card`

**Method:** `GET`

**Description:** This endpoint returns a 3 card Tarot reading. The cards are selected randomly from the deck and each card can be either upright or reversed.

**Web Page:** `/tarot/reading/3card_reading`

### 5 Card Reading

**Endpoint:** `/tarot/api/5card`

**Method:** `GET`

**Description:** This endpoint returns a 5 card Tarot reading. The cards are selected randomly from the deck and each card can be either upright or reversed.

**Web Page:** `/tarot/reading/5card`

## Setup

To set up the application, first install the required Python packages:

```bash
pip install -r requirements.txt