from dataclasses import dataclass
from typing import List


@dataclass
class Character:
    string: str
    code: int
    u_code: str
    name: str
    category: str
    combining: int


@dataclass
class GraphemeCluster:
    string: str
    base: Character
    modifiers: List[Character]

    @property
    def bsl(self):
        return self.base.string.lower()


@dataclass
class Token:
    string: str
    clusters: List[GraphemeCluster]


@dataclass
class WordToken(Token):
    pass


@dataclass
class Syllable:
    string: str
    onset: List[GraphemeCluster]
    nucleus: List[GraphemeCluster]
    coda: List[GraphemeCluster]
