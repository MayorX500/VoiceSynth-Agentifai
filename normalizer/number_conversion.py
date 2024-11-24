# modules/normalizer/number_conversion.py

import re
from typing import Any, Dict
from .base import NormalizationRule
import logging
import json

# Configure logging
logger = logging.getLogger(__name__)

class NumberConversionRule(NormalizationRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.enabled = config.get("enabled", False)
        if not self.enabled:
            return  # Early exit if number conversion is disabled

        number_config = config.get("normalize", {})
        self.detect_percentage = number_config.get("percentage", False)
        self.detect_years = number_config.get("years", False)
        self.detect_ordinal = number_config.get("ordinal", False)
        self.handle_fractions = number_config.get("fractions", False)
        self.handle_ranges = number_config.get("ranges", False)
        self.handle_currency = number_config.get("currency", False)
        self.amount_aware = config.get("amount_aware", False)
        self.supported_currency = config.get("supported_currency", [])
        self.currency_map_path = config.get("currency_map", "")
        self.type = config.get("type", "cardinal")

        # Load currency map
        with open(self.currency_map_path, 'r', encoding='utf-8') as f:
            self.currency_map = json.load(f)

        # Supported languages
        self.supported_languages = config.get("supported_languages", ["pt"])

        # Precompile regex patterns
        self.number_pattern = re.compile(r'\b\d+(\.\d+)?\b')
        self.currency_pattern = re.compile(r'([' + re.escape(''.join(self.supported_currency)) + r'])\s?\d+(\.\d+)?\b') # Currency symbol followed by a number with optional decimal #TODO: Number followed by currency symbol with optional decimal
        self.percentage_pattern = re.compile(r'\b(\d+(\.\d+)?)\s*%\b')
        self.year_pattern = re.compile(r'\b(19|20)\d{2}\b')
        self.ordinal_pattern = re.compile(r'\b\d+(º|ª|th)\b', re.IGNORECASE) #TODO: Per language matching
        self.fraction_pattern = re.compile(r'\b\d+/\d+\b') 
        self.range_pattern = re.compile(r'\b\d+\s*[-–]\s*\d+\b') #TODO: Add support for ranges with words (e.g., one to ten), Per language matching


        """for atrb in self.__dict__:
            print(f"{atrb}: {self.__dict__[atrb]}")"""

    def apply(self, text: str, language: str = 'pt') -> str:
        if not self.enabled:
            return text

        # Ensure language is supported
        if language not in self.supported_languages:
            return text

        # Normalize currencies first if handle_currency is enabled
        if self.handle_currency:
            text = self._normalize_currency(text, language)

        # Normalize percentages
        if self.detect_percentage:
            text = self._normalize_percentage(text, language)

        # Normalize years
        if self.detect_years:
            text = self._normalize_years(text, language)

        # Normalize ordinals
        if self.detect_ordinal:
            text = self._normalize_ordinals(text, language)

        # Normalize fractions
        if self.handle_fractions:
            text = self._normalize_fractions(text, language)

        # Normalize ranges
        if self.handle_ranges:
            text = self._normalize_ranges(text, language)

        # Normalize cardinals
        text = self._normalize_cardinals(text, language)

        return text

    def _normalize_currency(self, text: str, language: str) -> str:
        def replace_currency(match):
            symbol = match.group(1)
            amount = match.group(0).replace(symbol, '').strip()
            try:
                amount_num = float(amount)
                amount_word = self._number_to_words(amount_num, language)
                currency_info = self.currency_map.get(symbol, {})
                currency_names = currency_info.get(language, {})
                if amount_num == 1:
                    currency_name = currency_names.get("singular", symbol)
                else:
                    currency_name = currency_names.get("plural", symbol)
                return f"{amount_word} {currency_name}"
            except ValueError:
                return match.group(0)  # Return original if conversion fails

        return self.currency_pattern.sub(replace_currency, text)

    def _normalize_percentage(self, text: str, language: str) -> str:
        # FIX: dumb implementation, should be improved
        replacement = " por cento" if language == 'pt' else "percent"
        return text.replace('%', replacement)


    def _normalize_years(self, text: str, language: str) -> str:
        def replace_year(match):
            year = match.group(0)
            try:
                year_num = int(year)
                return self._year_to_words(year_num, language)
            except ValueError:
                return year
        return self.year_pattern.sub(replace_year, text)

    def _normalize_ordinals(self, text: str, language: str) -> str:
        def replace_ordinal(match):
            number = re.sub(r'(st|nd|rd|th)', '', match.group(0), flags=re.IGNORECASE)
            try:
                number_num = int(number)
                return self._ordinal_to_words(number_num, language)
            except ValueError:
                return match.group(0)
        return self.ordinal_pattern.sub(replace_ordinal, text)

    def _normalize_fractions(self, text: str, language: str) -> str:
        def replace_fraction(match_):
            fraction = match_.group(0)
            try:
                numerator, denominator = map(int, fraction.split('/'))
                numerator_word = self._number_to_words(numerator, language)
                denominator_word = self._number_to_words(denominator, language)
                match language:
                    case 'en':
                        return f"{numerator_word} over {denominator_word}"
                    case 'pt':
                        return f"{numerator_word} sobre {denominator_word}" #TODO: Add a better translation for this
            except ValueError:
                return fraction
        return self.fraction_pattern.sub(replace_fraction, text)

    def _normalize_ranges(self, text: str, language: str) -> str:
        def replace_range(match_):
            range_text = match_.group(0)
            parts = re.split(r'\s*[-–]\s*', range_text)
            if len(parts) == 2:
                try:
                    start = self._number_to_words(float(parts[0]), language)
                    end = self._number_to_words(float(parts[1]), language)
                    match language:
                        case 'en':
                            return f"{start} to {end}"
                        case 'pt':
                            return f"{start} a {end}"    
                except ValueError:
                    return range_text
            return range_text
        return self.range_pattern.sub(replace_range, text)

    def _normalize_cardinals(self, text: str, language: str) -> str:
        def replace_number(match):
            number = match.group(0)
            try:
                number_num = float(number)
                return self._number_to_words(number_num, language)
            except ValueError:
                return number
        return self.number_pattern.sub(replace_number, text)

    def _number_to_words(self, number: float, language: str) -> str:
        """
        Convert a number to its word representation.
        For simplicity, we'll use the `num2words` library.
        """
        try:
            from num2words import num2words
            return num2words(number, lang=language)
        except ImportError:
            # Fallback if num2words is not installed
            return str(number)

    def _year_to_words(self, year: int, language: str) -> str:
        """
        Convert a year to words. E.g., 2024 -> two thousand twenty-four
        """
        return self._number_to_words(year, language)

    def _ordinal_to_words(self, number: int, language: str) -> str:
        """
        Convert an ordinal number to words. E.g., 1st -> first
        """
        try:
            from num2words import num2words
            return num2words(number, to='ordinal', lang=language)
        except ImportError:
            # Fallback if num2words is not installed
            return f"{number}th" # TODO: Bad fallback, improve this
