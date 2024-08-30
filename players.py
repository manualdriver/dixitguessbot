import random
from typing import Tuple, Optional, List
from model_manager import ModelManager
from generate_image_caption import ImageCaptionGenerator
from similarity import ImageTextSimilarity

class Bot:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = model_manager
        self._caption_generator = ImageCaptionGenerator(self._model_manager)
        self._similarity_checker = ImageTextSimilarity(self._model_manager)

    def choose_card_based_on_clue(self, clue: str, deck: List[str]) -> Tuple[float, str]:
        similarities = [
            (self._similarity_checker.compare_image_and_text(card, clue), card)
            for card in deck
        ]

        if not similarities:
            print(f"Gusser could not find any matching cards based on the clue. Returning random card")
            return self.choose_random_card(deck)

        best_match = max(similarities, key=lambda x: x[0])
        return best_match

    def choose_random_card(self, deck: List[str]) -> str:
        chosen_card = random.choice(deck)
        return chosen_card
