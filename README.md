# Flask Tarot API

This Flask application provides a Tarot card reading API and web interface. It uses a JSON file to load a Tarot deck and provides two API endpoints and corresponding web pages for different types of readings. The application also includes a feature to convert the AI-generated reading from Markdown to HTML and display it on the web page with proper indentation.

## API Endpoints

### 3 Card Reading

**Endpoint:** `http://<your-host-ip>:8080/tarot/api/3card`

**Method:** `GET`

**Description:** This endpoint returns a 3 card Tarot reading. The cards are selected randomly from the deck and each card can be either upright or reversed.

**Web Page:** `http://<your-host-ip>:8080/tarot/reading/3card`

### 5 Card Reading

**Endpoint:** `http://<your-host-ip>:8080/tarot/api/5card`

**Method:** `GET`

**Description:** This endpoint returns a 5 card Tarot reading. The cards are selected randomly from the deck and each card can be either upright or reversed.

**Web Page:** `http://<your-host-ip>:8080/tarot/reading/5card`

## Setup

To set up the application, first install the required Python packages:

```bash
pip install -r requirements.txt