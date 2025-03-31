import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from flask_tarot_gen import get_interpretation

def test_tarot_reading():
    test_cards = [
        {"card_name": "The Fool", "orientation": "upright"},
        {"card_name": "The Star", "orientation": "reversed"},
        {"card_name": "The Moon", "orientation": "upright"}
    ]

    interpretation = get_interpretation(test_cards, "3card")
    print(interpretation)

if __name__ == "__main__":
    test_tarot_reading()