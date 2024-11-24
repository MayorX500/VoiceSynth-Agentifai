import re
import json
import os
import logging
from .base import NormalizationRule

logger = logging.getLogger(__name__)

class CustomReplacementRule(NormalizationRule):
    def __init__(self, config):
        super().__init__(config)
        self.enabled = config.get('enabled', False)
        self.mapped_replacements = None
        self.load_replacements()

    def load_replacements(self):
        config = self.config
        # Load abreveations from external file abbreviation_file
        external_mapping_file = config.get('custom_replacement_file', None)
        if external_mapping_file:
            try:
                with open(external_mapping_file, 'r') as f:
                    self.mapped_replacements = json.load(f)
            except Exception as e:
                print(f"Failed to load external replacements from {external_mapping_file}: {e}")
                self.mapped_replacements = {}

    def apply(self, text, language='pt'):
        config = self.config
        if self.enabled and (self.mapped_replacements is not None):
            replacements = self.mapped_replacements.get(language, [])

            flags = 0
            if not config.get('case_sensitive', False):
                flags |= re.IGNORECASE
            if config.get('use_regex_flags', False):
                flags |= re.UNICODE
            
            for item in replacements:
                pattern = item.get('pattern')
                replacement = item.get('replacement', '')
                try:
                    text = re.sub(pattern, replacement, text, flags=flags)
                except re.error as e:
                    logger.error(f"Invalid regex pattern '{pattern}': {e}")
        return text