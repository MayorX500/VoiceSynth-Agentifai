# modules/normalizer/base.py

from abc import ABC, abstractmethod

class NormalizationRule(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def apply(self, text, locale='pt'):
        """
        Apply the normalization rule to the given text.
        Must be implemented by subclasses.
        """
        pass
