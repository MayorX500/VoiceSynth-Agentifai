# dev.py

from modules.normalizer import Normalizer
import os

def main():
    # Define the path to the normalization rules TOML file
    # Assuming 'config' directory is at the root of the project
    rules_file = os.path.join('config', 'normalization_rules.toml')

    # Initialize the Normalizer
    normalizer = Normalizer(rules_file)

    # Example texts to normalize
    test_texts = [
        "Dr. Smith earned 50% of the $1000 revenue on 2023-04-15.",
        "I have 2 apples and 3 oranges.",
        "The event is scheduled for 15/04/2023.",
        "CEO and AI are important terms.",
        "Please call me at 555-1234.",
        "Mrs. Johnson lives on St. Patrick's Street.",
        "She finished 1st in the race.",
        "The ratio is 3/4.",
        "The years 1999-2003 were challenging."
    ]

    # Normalize each text
    for text in test_texts:
        normalized = normalizer.normalize_text(text)
        print(f"Original: {text}")
        print(f"Normalized: {normalized}\n")

if __name__ == "__main__":
    main()
