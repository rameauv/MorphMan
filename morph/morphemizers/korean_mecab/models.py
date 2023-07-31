from abc import abstractmethod, ABC


class AddonMorphzMorph(ABC):
    @abstractmethod
    def __init__(self):
        self.word: str = ""
        self.pos: str = ""
        self.subPos: str = ""
        self.norm: str = ""
        self.base: str = ""
        self.inflected: str = ""
        self.read: str = ""


class MecabController(ABC):
    @abstractmethod
    def spawn_mecab(self):
        # type: () -> subprocess.Popen
        raise NotImplementedError()

    @abstractmethod
    def dispose_mecab(self):
        pass

    @abstractmethod
    def get_morphemes(self, expression):
        # type: (str) -> list[AddonMorphzMorph]
        raise NotImplementedError()

    @abstractmethod
    def get_description(self):
        # type: () -> str
        """
        Returns a single line, for which languages this Morphemizer is.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_name(self):
        # type: () -> str
        raise NotImplementedError()
