import importlib

from .korean_mecab_morphemizer import KoreanMecabMorphemizer
from .placeholder_morphemizer import PlaceholderMorphemizer


def korean_mecab_morphemizer_provider():
    try:
        module = importlib.import_module('morphman_korean_mecab')
        return KoreanMecabMorphemizer(module)
    except ModuleNotFoundError as e:
        print("korean_mecab_morphemizer not found")
        return PlaceholderMorphemizer(e)
