# -*- coding: utf-8 -*-

from .morphemizers import \
    JiebaMorphemizer, \
    MecabMorphemizer, \
    SpaceMorphemizer, \
    CjkCharMorphemizer, \
    korean_mecab_morphemizer_provider

####################################################################################################
# Morphemizer Helpers
####################################################################################################

morphemizers = None
morphemizers_by_name = {}


def getAllMorphemizers():
    # type: () -> [Morphemizer]
    global morphemizers
    if morphemizers is None:
        morphemizers = [
            SpaceMorphemizer(),
            MecabMorphemizer(),
            JiebaMorphemizer(),
            CjkCharMorphemizer(),
            korean_mecab_morphemizer_provider(),
        ]

        for m in morphemizers:
            morphemizers_by_name[m.getName()] = m

    return morphemizers


def getMorphemizerByName(name):
    # type: (str) -> Optional(Morphemizer)
    getAllMorphemizers()
    return morphemizers_by_name.get(name, None)
