from typing import List

import os
from config import settings


def load_forbidden_words() -> list[str]:
    forbidden_words_file = os.path.join(settings.BASE_DIR, 'base', 'static', 'words.txt')
    with open(forbidden_words_file, 'r') as file:
        forbidden_word = file.read().splitlines()
    return forbidden_word


def contains_forbidden_words(text: str, forbidden_words: List[str]) -> bool:
    text_word = set(text.lower().split())
    forbidden_set = set(item.lower() for item in forbidden_words)
    return bool(text_word.intersection(forbidden_set))
