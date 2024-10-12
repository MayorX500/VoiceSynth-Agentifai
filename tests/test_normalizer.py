# tests/test_normalizer.py

import unittest
from modules.normalizer import Normalizer
import os

class TestNormalizer(unittest.TestCase):
    def setUp(self):
        pass  # Individual tests will handle setup

    def load_normalizer(self, config_filename, rules=None):
        # Path to the main configuration file
        config_path = os.path.join('tests/config', config_filename)
        return Normalizer(config_path, enabled_rules=rules)
    
    def test_abbreviations(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["abbreviations"])
        input_text = "Dr. Smith lives on St. Patrick's Street."
        expected = "Doctor Smith lives on Saint Patrick's Street."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_number_conversion_cardinal(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["number_conversion"])
        input_text = "I have 2 apples and 3 oranges."
        expected = "I have two apples and three oranges."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    #TODO: Add Phone Number Conversion to normalization_rules.toml and Normalizer module
    def test_phone_number_conversion(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Please call me at 555-1234."
        expected = "Please call me at five five five one two three four."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_number_conversion_percentage(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["number_conversion"])
        input_text = "She scored 85% on her test."
        expected = "She scored eighty-five percent on her test."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_number_conversion_currency(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["number_conversion"])
        input_text = "The cost is $2500."
        expected = "The cost is two thousand five hundred dollars."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_number_conversion_ordinal(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["number_conversion"])
        input_text = "He finished 1st in the race."
        expected = "He finished first in the race."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_number_conversion_fraction(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["number_conversion"])
        input_text = "The ratio is 3/4."
        expected = "The ratio is three over four."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_number_conversion_range(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["number_conversion"])
        input_text = "The years 1999-2003 were challenging."
        expected = "The years from one thousand nine hundred and ninety-nine to two thousand and three were challenging."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_date_conversion_full_date(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["date_conversion"])
        input_text = "The meeting is on 2023-04-15."
        expected = "The meeting is on April fifteenth, twenty twenty-three."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_date_conversion_partial_date(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["date_conversion"])
        input_text = "The event is scheduled for January 2020."
        expected = "The event is scheduled for January twenty twenty."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_custom_replacements(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["custom_replacements"])
        input_text = "AI and CEO are crucial."
        expected = "Artificial Intelligence and Chief Executive Officer are crucial."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
        
    def test_punctuation_handling(self):
        normalizer = self.load_normalizer('normalization_rules.toml', rules=["punctuation_handling"])
        input_text = "Hello, world. Please call me at 555-1234."
        expected = "Hello world. Please call me at 555-1234."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_combined_rules(self):
        # To test combined rules, enable all necessary rules
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Dr. Johnson earned 75% of the €2000 on 15/04/2023."
        expected = "Doctor Johnson earned seventy-five percent of the two thousand euros on April fifteenth twenty twenty-three."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
