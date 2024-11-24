# tests/test_normalizer.py
import sys
sys.path.append('..')  # Adiciona o diretório pai ao caminho de importação


import unittest
from normalizer import TextNormalizer as Normalizer
import os

class TestNormalizer(unittest.TestCase):
    def setUp(self):
        pass  # Cada teste individual lidará com a configuração

    def load_normalizer(self, config_filename, rules=None):
        # Caminho para o arquivo de configuração principal
        config_path = os.path.join('config', config_filename)
        return Normalizer(config_path)



    def test_number_conversion_currency(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "O custo é de €2500."
        expected = "O custo é de dois mil e quinhentos euros."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
"""
    
    def test_number_conversion_ordinal(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Ele terminou em 1º lugar na corrida."
        expected = "Ele terminou em primeiro lugar na corrida."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_number_conversion_fraction(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "A proporção é de 3/4."
        expected = "A proporção é de três sobre quatro."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_number_conversion_range(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Os anos de 1999-2003 foram desafiadores."
        expected = "Os anos de mil novecentos e noventa e nove a dois mil e três foram desafiadores."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_date_conversion_full_date(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "A reunião é em 2023-04-15."
        expected = "A reunião é em Abril quinze, dois mil e vinte e três."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
    
    def test_date_conversion_partial_date(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "O evento está agendado para Janeiro 2020."
        expected = "O evento está agendado para Janeiro dois mil e vinte."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_custom_replacements(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "AI e CEO são cruciais."
        expected = "Inteligência Artificial e Diretor Executivo são cruciais."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
        
    def test_punctuation_handling(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Olá, mundo. Por favor, ligue para 555-1234."
        expected = "Olá mundo. Por favor, ligue para 555-1234."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_combined_rules(self):
        # Para testar regras combinadas, habilite todas as regras necessárias
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Dr. João ganhou 75% dos €2000 em 15/04/2023."
        expected = "Doutor João ganhou setenta e cinco por cento dos dois mil euros em Abril quinze dois mil e vinte e três."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

------

    def test_abbreviations(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Dr. Silva vive na Rua St. António."
        expected = "Doutor Silva vive na Rua Santo António."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

        
    def test_number_conversion_cardinal(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Eu tenho 2 maçãs e 3 laranjas."
        # TODO: The normalization rules are not gender-aware
        expected = "Eu tenho dois maçãs e três laranjas."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)

    def test_number_conversion_percentage(self):
        normalizer = self.load_normalizer('normalization_rules.toml')
        input_text = "Ela obteve 85% no teste."
        expected = "Ela obteve oitenta e cinco por cento no teste."
        result = normalizer.normalize_text(input_text)
        self.assertEqual(result, expected)
"""
        
if __name__ == "__main__":
    unittest.main()

