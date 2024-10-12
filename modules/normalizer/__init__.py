# modules/normalizer/__init__.py

from .number_conversion import NumberConversion
from .date_conversion import DateConversion
from .abbreviations import Abbreviations
from .custom_replacements import CustomReplacements
from .punctuation_handling import PunctuationHandling
import tomli
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('normalizer')

class Normalizer:
    def __init__(self, rules_file_path, enabled_rules=None):
        self.rules_config = self.load_rules(rules_file_path)
        self.all_rule_order = self.rules_config.get('rule_order', [])
        self.enabled_rules = enabled_rules if enabled_rules is not None else self.all_rule_order
        self.rules = self.initialize_rules()

    def load_rules(self, file_path):
        try:
            # Resolve the absolute path relative to the current script
            abs_path = os.path.abspath(file_path)
            with open(abs_path, 'rb') as file:
                return tomli.load(file)
        except Exception as e:
            logger.error(f"Error loading rules file '{file_path}': {e}")
            return {}

    def initialize_rules(self):
        # Initialize each rule with the relevant configuration
        rules_config = self.rules_config.get('rules', {})
        rule_objects = {}
        for rule_name in self.enabled_rules:
            rule_config = rules_config.get(rule_name, {})
            if rule_config.get('enabled', False):
                if rule_name == "date_conversion":
                    rule_objects[rule_name] = DateConversion(rule_config)
                elif rule_name == "number_conversion":
                    rule_objects[rule_name] = NumberConversion(rule_config)
                elif rule_name == "abbreviations":
                    rule_objects[rule_name] = Abbreviations(rule_config)
                elif rule_name == "custom_replacements":
                    rule_objects[rule_name] = CustomReplacements(rule_config)
                elif rule_name == "punctuation_handling":
                    rule_objects[rule_name] = PunctuationHandling(rule_config)
                else:
                    logger.warning(f"Unknown rule '{rule_name}' in configuration.")
        return rule_objects

    def normalize_text(self, text):
        for rule_name in self.enabled_rules:
            rule = self.rules.get(rule_name)
            if rule:
                logger.debug(f"Applying rule: {rule_name}")
                text = rule.apply(text)
        return text
