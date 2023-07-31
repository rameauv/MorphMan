from ...morphemizer import Morphemizer


class PlaceholderMorphemizer(Morphemizer):

    def __init__(self, e):
        # type: (ModuleNotFoundError) -> None
        self.e = e

    def _getMorphemesFromExpr(self, expression):
        # type: (str) -> [Morpheme]
        raise OSError('''
            Mecab Korean analyzer could not be found.
            Please install the following Anki add-ons:
            https://github.com/rameauv/morphman_korean_mecab''') from self.e

    def getDescription(self):
        # type: () -> str
        """
        Returns a single line, for which languages this Morphemizer is.
        """
        return 'Korean mecab UNAVAILABLE'

    def getName(self):
        # type: () -> str
        return 'Korean mecab UNAVAILABLE'
