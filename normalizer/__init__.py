import toml
import json

from .base import NormalizationRule
from .abbreviations import AbbreviationRule
from .custom_replacements import CustomReplacementRule
from .number_conversion import NumberConversionRule
from .punctuation_handling import PunctuationHandlingRule
from .date_conversion import DateConversionRule

class TextNormalizer:
    rules_config: dict
    rules: list[NormalizationRule]

    def __init__(self, rules_files):
        self.rules_config = toml.load(rules_files)
        self.rules = []

        if self.rules_config['rules']['custom_replacements']['enabled']:
            self.rules.append(CustomReplacementRule(self.rules_config['rules']['custom_replacements']))

        if self.rules_config['rules']['abbreviations']['enabled']:
            self.rules.append(AbbreviationRule(self.rules_config['rules']['abbreviations']))

        if self.rules_config['rules']['number_conversion']['enabled']:
            self.rules.append(NumberConversionRule(self.rules_config['rules']['number_conversion']))

        if self.rules_config['rules']['date_conversion']['enabled']:
            self.rules.append(DateConversionRule(self.rules_config['rules']['date_conversion']))

        if self.rules_config['rules']['punctuation_handling']['enabled']:
            self.rules.append(PunctuationHandlingRule(self.rules_config['rules']['punctuation_handling']))

    def load_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def normalize_text(self, text, lang_code='pt'):
        if lang_code not in self.rules_config['supported_languages']:
            raise ValueError(f"Language code {lang_code} not supported")
        for rule in self.rules:
            text = rule.apply(text, lang_code)
        return text