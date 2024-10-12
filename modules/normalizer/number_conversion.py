# modules/normalizer/number_conversion.py

import re
from num2words import num2words
from .base import NormalizationRule
import logging

# Configure logging
logger = logging.getLogger(__name__)

class NumberConversion(NormalizationRule):
    def apply(self, text):
        config = self.config
        if not config.get('enabled', False):
            return text

        locale = config.get('locale', 'en')
        type_ = config.get('type', 'cardinal')
        supported_currency = config.get('supported_currency', ["$", "€"])

        # Handle currency
        if config.get('handle_currency', False):
            for symbol in supported_currency:
                coin = "dollar" if symbol == "$" else "euro"
                pattern = re.escape(symbol) + r"(\d+(\.\d+)?)"
                matches = re.finditer(pattern, text)
                for match in matches:
                    amount = match.group(1)
                    try:
                        amount_float = float(amount)
                        # Convert to integer if possible
                        if amount_float >1:
                            coin = "dollars" if symbol == "$" else "euros"
                        if amount_float.is_integer():
                            amount_word = num2words(int(amount_float), lang=locale)
                        else:
                            amount_word = num2words(amount_float, lang=locale)
                        replacement = f"{amount_word.replace(",","")} {coin}"
                        text = text.replace(match.group(0), replacement)
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Failed to convert currency amount '{match.group(0)}': {e}")
                        continue  # Skip if conversion fails

        # Handle percentages
        if config.get('detect_percentage', False):
            pattern = r'(\d+(\.\d+)?)\s?%'
            matches = re.finditer(pattern, text)
            for match in matches:
                number = match.group(1)
                try:
                    number_float = float(number)
                    # Convert to integer if possible
                    if number_float.is_integer():
                        number_word = num2words(int(number_float), lang=locale)
                    else:
                        number_word = num2words(number_float, lang=locale)
                    replacement = f"{number_word.replace(",","")} percent"
                    text = text.replace(match.group(0), replacement)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to convert percentage '{match.group(0)}': {e}")
                    continue

        # Handle ordinals
        if config.get('detect_ordinal', False):
            pattern = r'\b(\d+)(st|nd|rd|th)\b'
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                number = int(match.group(1))
                try:
                    ordinal_word = num2words(number, to='ordinal', lang=locale)
                    text = text.replace(match.group(0), ordinal_word)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to convert ordinal '{match.group(0)}': {e}")
                    continue

        # Handle fractions
        if config.get('handle_fractions', False):
            pattern = r'\b(\d+)/(\d+)\b'
            matches = re.finditer(pattern, text)
            for match in matches:
                numerator = match.group(1)
                denominator = match.group(2)
                try:
                    numerator_word = num2words(int(numerator), lang=locale)
                    denominator_word = num2words(int(denominator), lang=locale)
                    fraction_word = f"{numerator_word} over {denominator_word}"
                    text = text.replace(match.group(0), fraction_word)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to convert fraction '{match.group(0)}': {e}")
                    continue

        # Handle ranges
        if config.get('handle_ranges', False):
            pattern = r'\b(\d+)\s?[-–]\s?(\d+)\b'
            matches = re.finditer(pattern, text)
            for match in matches:
                start = match.group(1)
                end = match.group(2)
                try:
                    start_num = int(start)
                    end_num = int(end)
                    start_word = num2words(start_num, lang=locale)
                    end_word = num2words(end_num, lang=locale)
                    range_word = f"from {start_word.replace(",","")} to {end_word.replace(",","")}"
                    text = text.replace(match.group(0), range_word)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to convert range '{match.group(0)}': {e}")
                    continue

        # Handle cardinal numbers
        if type_ == "cardinal":
            pattern = r'\b\d+\b'
            matches = re.finditer(pattern, text)
            for match in matches:
                number = int(match.group(0))
                try:
                    number_word = num2words(number, lang=locale)
                    text = text.replace(match.group(0), number_word.replace(",",""))
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to convert number '{match.group(0)}': {e}")
                    continue

        return text

    def convert_year_to_words(self, year_str, locale):
        year = int(year_str)
        if 2000 <= year <= 2099:
            first_part = num2words(year // 100, lang=locale)
            second_part = num2words(year % 100, lang=locale)
            return f"{first_part} {second_part}"
        else:
            return num2words(year, lang=locale)
