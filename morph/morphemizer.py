# -*- coding: utf-8 -*-
from functools import lru_cache

from .morphemes import Morpheme

####################################################################################################
# Base Class
####################################################################################################

class Morphemizer:
    def __init__(self):
        pass
    
    @lru_cache(maxsize=131072)
    def getMorphemesFromExpr(self, expression):
        # type: (str) -> [Morpheme]
        
        morphs = self._getMorphemesFromExpr(expression)
        return morphs
    
    def _getMorphemesFromExpr(self, expression):
        # type: (str) -> [Morpheme]
        """
        The heart of this plugin: convert an expression to a list of its morphemes.
        """
        return []

    def getDescription(self):
        # type: () -> str
        """
        Returns a single line, for which languages this Morphemizer is.
        """
        return 'No information available'

    def getName(self):
        # type: () -> str
        return self.__class__.__name__
