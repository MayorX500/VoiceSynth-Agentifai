# modules/normalizer/punctuation_handling.py

import re
from base import NormalizationRule

class PunctuationHandling(NormalizationRule):
    def apply(self, text, locale='pt'):
        config = self.config
        if not config.get('enabled', False):
            return text
        remove = config.get('remove', [])
        replace_with_space = config.get('replace_with_space', [])

        for punct in remove:
            text = text.replace(punct, '')

        for punct in replace_with_space:
            text = text.replace(punct, ' ')

        # Normalize multiple spaces to single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text
