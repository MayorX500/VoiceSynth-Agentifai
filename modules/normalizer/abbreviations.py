# modules/normalizer/abbreviations.py

import re
import json
from .base import NormalizationRule

class Abbreviations(NormalizationRule):
    def __init__(self, config):
        super().__init__(config)
        self.abbrev_mapping = {}
        self.load_mappings()

    def load_mappings(self):
        abbrev_config = self.config
        if not abbrev_config.get('enabled', False):
            return

        # Load internal mappings
        self.abbrev_mapping = abbrev_config.get('mapping', {})

        # Load external abbreviations if enabled
        if abbrev_config.get('external_abreviations', False):
            abbrev_file = abbrev_config.get('abbreviation_file', 'abbreviations.json')
            try:
                with open(abbrev_file, 'r') as f:
                    external_mapping = json.load(f)
                    self.abbrev_mapping.update(external_mapping)
            except Exception as e:
                print(f"Failed to load external abbreviations from {abbrev_file}: {e}")

    def apply(self, text):
        if not self.abbrev_mapping:
            return text

        for abbr, full in self.abbrev_mapping.items():
            # Adjusting the pattern to correctly match abbreviations with period
            pattern = r'\b' + re.escape(abbr[:-1]) + r'\.'
            text = re.sub(pattern, full, text)

        return text
