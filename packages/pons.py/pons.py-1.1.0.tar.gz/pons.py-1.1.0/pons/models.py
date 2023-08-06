from dataclasses import dataclass, is_dataclass
from typing import Any, Dict, List, Literal, Optional

__all__ = (
    "Language",
    # dictionaries
    "Dictionary",
    # querying
    "Translation",
    "Arab",
    "Rom",
    "Hit",
    "EntryHit",
    "TranslationHit",
    "NestedEntryHit",
    "create_hit",
)


Language = Literal[
    "de", "el", "en", "es", "fr", "it", "pl", "pt", "ru", "sl", "tr", "zh"
]


@dataclass(repr=False)
class Dictionary:
    key: str
    simple_label: str
    directed_label: Dict[str, str]
    languages: List[Language]

    def __repr__(self) -> str:
        return f"Dictionary(key='{self.key}')"


@dataclass(repr=False)
class Translation:
    source: str
    target: str

    def __repr__(self) -> str:
        return "Translation()"


class Arab:
    header: str
    translations: List[Translation]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.header = data["header"]
        self.translations = [
            Translation(**translation) for translation in data["translations"]
        ]

    def __repr__(self) -> str:
        return f"Arab(header='{self.header}')"


class Rom:
    headword: str
    headword_full: str
    wordclass: Optional[str]
    arabs: List[Arab]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.headword = data["headword"]
        self.headword_full = data["headword_full"]
        self.wordclass = data["wordclass"]
        self.arabs = [Arab(arab) for arab in data["arabs"]]

    def __repr__(self) -> str:
        return f"Rom(headword='{self.headword}')"


class Hit:
    type: Literal["entry", "translation", "entry_with_secondary_entries"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class EntryHit(Hit):
    type = "entry"
    opendict: bool
    roms: List[Rom]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.opendict = data["opendict"]
        self.roms = [Rom(rom) for rom in data["roms"]]

    @property
    def translations(self) -> List[str]:
        to_return = []
        for rom in self.roms:
            for arab in rom.arabs:
                for translation in arab.translations:
                    to_return.append(translation.target)
        return to_return


@dataclass(repr=False)
class TranslationHit(Hit, Translation):
    type = "translation"
    opendict: bool


class NestedEntryHit(Hit):
    type = "entry_with_secondary_entries"
    primary: EntryHit
    secondary: List[EntryHit]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.primary = EntryHit(data["primary_entry"])
        self.secondary = [EntryHit(entry) for entry in data["secondary_entries"]]


def create_hit(data: Dict[str, Any]) -> Hit:
    hit_types = {cls.type: cls for cls in [EntryHit, TranslationHit, NestedEntryHit]}
    cls = hit_types[data.pop("type")]
    if is_dataclass(cls):
        return cls(**data)
    return cls(data)
