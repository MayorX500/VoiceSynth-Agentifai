# modules/normalizer/custom_replacements.py

import re
from .base import NormalizationRule

class CustomReplacements(NormalizationRule):
    def apply(self, text):
        config = self.config
        if not config.get('enabled', False):
            return text

        patterns = config.get('patterns', [])
        case_sensitive = config.get('case_sensitive', False)
        use_regex_flags = config.get('use_regex_flags', False)

        flags = 0
        if not case_sensitive:
            flags |= re.IGNORECASE
        if use_regex_flags:
            flags |= re.UNICODE  # Add more flags if necessary

        for item in patterns:
            pattern = item.get('pattern')
            replacement = item.get('replacement', '')
            try:
                text = re.sub(pattern, replacement, text, flags=flags)
            except re.error as e:
                print(f"Invalid regex pattern '{pattern}': {e}")

        return text
