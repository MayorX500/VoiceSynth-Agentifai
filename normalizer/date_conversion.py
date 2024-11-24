# modules/normalizer/date_conversion.py

import re
import dateparser
from .base import NormalizationRule
from num2words import num2words


class DateConversionRule(NormalizationRule):
    def apply(self, text, language='pt'):
        config = self.config
        if not config.get('enabled', False):
            return text

        formats = config.get('formats', [])
        allowed_separators = config.get('allowed_separator', ["-", "/", ".", " "])
        allow_partial = config.get('allow_partial_dates', False)

        # Handle partial dates
        success = False
        if allow_partial:
            # Example: "Janeiro 2020" for Portuguese
            # Find only months and years
            partial_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro)\b\s+\d{4}'
            try:
                partial_matches = re.finditer(partial_pattern, text)
            except re.error as e:
                partial_matches = []

            for match in partial_matches:
                date_str = match.group(0)
                parsed_date = dateparser.parse(date_str, languages=[language])
                if parsed_date:
                    date_word = parsed_date.strftime("%B %Y")
                    date_list = date_word.split(" ")
                    if len(date_list) == 2:
                        date_list[1] = num2words(int(date_list[1]), to='year', lang=language)
                        date_word = " ".join(date_list)
                    text = text.replace(date_str, date_word)
                    success = True

        if success:
            return text

        # Build regex patterns based on formats
        date_patterns = []
        for fmt in formats:
            # Replace (sep) with allowed separators
            sep_pattern = f"[{''.join(map(re.escape, allowed_separators))}]"
            fmt_regex = re.escape(fmt).replace('\\(sep\\)', sep_pattern)
            # Replace tokens with regex patterns without named groups
            fmt_regex = fmt_regex.replace("yyyy", r"\d{4}")
            fmt_regex = fmt_regex.replace("yy", r"\d{2}")
            fmt_regex = fmt_regex.replace("MM", r"\d{2}")
            fmt_regex = fmt_regex.replace("dd", r"\d{2}")
            date_patterns.append(fmt_regex)

        combined_pattern = "|".join(date_patterns)
        try:
            matches = re.finditer(combined_pattern, text)
        except re.error as e:
            return text

        for match in matches:
            date_str = match.group(0)
            parsed_date = dateparser.parse(date_str, languages=[language])
            if parsed_date:
                date_word = parsed_date.strftime("%B %d, %Y")
                date_list = date_word.split(" ")
                if len(date_list) == 3:
                    date_list[1] = num2words(int(date_list[1].replace(",", "")), to='ordinal', lang=language)
                    date_list[1] = date_list[1] + ","
                    date_list[2] = num2words(int(date_list[2]), to='year', lang=language)
                    date_word = " ".join(date_list)
                text = text.replace(date_str, date_word)

        return text