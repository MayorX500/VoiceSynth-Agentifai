# modules/normalizer/abbreviations.py

import re
import json
from .base import NormalizationRule

class AbbreviationRule(NormalizationRule):
    def __init__(self, config):
        super().__init__(config)
        self.enabled = config.get('enabled', False)
        self.abbrev_mapping = None
        self.load_mappings()

    def load_mappings(self):
        abbrev_config = self.config
        if not abbrev_config.get('enabled', False):
            return

        # Load abreveations from external file abbreviation_file
        external_mapping_file = abbrev_config.get('abbreviation_file', None)
        if external_mapping_file:
            try:
                with open(external_mapping_file, 'r') as f:
                    self.abbrev_mapping = json.load(f)
            except Exception as e:
                print(f"Failed to load external abbreviations from {external_mapping_file}: {e}")
                self.abbrev_mapping = {}

    def apply(self, text, language='pt'):
        if self.enabled and (self.abbrev_mapping is not None):
            for abbr, full in self.abbrev_mapping.get(language, {}).items():
                # the pattern is a string that matches the abbreviation as a whole word example: "Dr.": "Doutor"
                pattern = rf'\b{re.escape(abbr)}?\b'
                text = re.sub(pattern, full, text) 
                ## there is a point in the end of the full word in the final text that shouldn't be there
                text = re.sub(rf'{full}\.', full, text)

        return text
