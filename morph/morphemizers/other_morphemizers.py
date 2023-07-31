import re

from ..deps.jieba import posseg
from ..deps.zhon.hanzi import characters
from ..mecab_wrapper import getMorphemesMecab, getMecabIdentity
from ..morphemes import Morpheme
from ..morphemizer import Morphemizer

####################################################################################################
# Mecab Morphemizer
####################################################################################################

space_char_regex = re.compile(' ')

class MecabMorphemizer(Morphemizer):
    """
    Because in japanese there are no spaces to differentiate between morphemes,
    a extra tool called 'mecab' has to be used.
    """

    def _getMorphemesFromExpr(self, expression):
        # Remove simple spaces that could be added by other add-ons and break the parsing.
        if space_char_regex.search(expression):
            expression = space_char_regex.sub('', expression)

        return getMorphemesMecab(expression)

    def getDescription(self):
        try:
            identity = getMecabIdentity()
        except:
            identity = 'UNAVAILABLE'
        return 'Japanese ' + identity


####################################################################################################
# Space Morphemizer
####################################################################################################

class SpaceMorphemizer(Morphemizer):
    """
    Morphemizer for languages that use spaces (English, German, Spanish, ...). Because it is
    a general-use-morphemizer, it can't generate the base form from inflection.
    """

    def _getMorphemesFromExpr(self, expression):
        word_list = [word.lower()
                     for word in re.findall(r"\b[^\s\d]+\b", expression, re.UNICODE)]
        return [Morpheme(word, word, word, word, 'UNKNOWN', 'UNKNOWN') for word in word_list]

    def getDescription(self):
        return 'Language w/ Spaces'


####################################################################################################
# CJK Character Morphemizer
####################################################################################################

class CjkCharMorphemizer(Morphemizer):
    """
    Morphemizer that splits sentence into characters and filters for Chinese-Japanese-Korean logographic/idiographic
    characters.
    """

    def _getMorphemesFromExpr(self, expression):
        return [Morpheme(character, character, character, character, 'CJK_CHAR', 'UNKNOWN') for character in
                re.findall('[%s]' % characters, expression)]

    def getDescription(self):
        return 'CJK Characters'


####################################################################################################
# Jieba Morphemizer (Chinese)
####################################################################################################

class JiebaMorphemizer(Morphemizer):
    """
    Jieba Chinese text segmentation: built to be the best Python Chinese word segmentation module.
    https://github.com/fxsjy/jieba
    """

    def _getMorphemesFromExpr(self, expression):
        # remove all punctuation
        expression = ''.join(re.findall('[%s]' % characters, expression))
        return [Morpheme(m.word, m.word, m.word, m.word, m.flag, 'UNKNOWN') for m in
                posseg.cut(expression)]  # find morphemes using jieba's POS segmenter

    def getDescription(self):
        return 'Chinese'
