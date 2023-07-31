from types import ModuleType

from ...morphemes import Morpheme
from ...morphemizer import Morphemizer
from .models import AddonMorphzMorph, MecabController
from ...util_external import memoize


class KoreanMecabMorphemizer(Morphemizer):
    """
    A morphemizer of the Korean language that use a fork a tool called Mecab
    originally made for Japanese but adapted to work with Korean.
    TODO indicate the proper addon
    An anki addon is needed for it to work
    """

    def __init__(self, controller):
        # type: (ModuleType) -> None
        super().__init__()
        self.module = controller

    def _getMorphemesFromExpr(self, expression):
        # type: (str) -> list[Morpheme]
        res = self._get_morphemes_mecab(expression)
        return res

    def getDescription(self):
        # type: () -> str
        controller: MecabController = self._get_mecab_controller_instance()
        return controller.get_description()

    def getName(self):
        # type: () -> str
        controller: MecabController = self._get_mecab_controller_instance()
        return controller.get_name()

    @memoize
    def _get_mecab_controller_instance(self):
        # type: () -> MecabController
        mecab_wrapper: MecabController = self.module.Controller()
        mecab_wrapper.spawn_mecab()

        return mecab_wrapper

    @memoize
    def _get_morphemes_mecab(self, expression):
        # type: (str) -> list[Morpheme]
        mecab_controller: MecabController = self._get_mecab_controller_instance()
        addon_morphemes = mecab_controller.get_morphemes(expression)
        morphemes = list(map(_map_addon_morpheme_to_morpheme, addon_morphemes))
        return morphemes


def _map_addon_morpheme_to_morpheme(morph):
    # type: (AddonMorphzMorph) -> Morpheme
    return Morpheme(
        norm=morph.norm,
        inflected=morph.inflected,
        pos=morph.pos,
        subPos=morph.subPos,
        base=morph.base,
        read=morph.read
    )
