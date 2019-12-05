import unicodedata
from typing import List

from dclasses import Character, GraphemeCluster, Token, WordToken


def characters(s: str) -> List[Character]:

    return [
        Character(
            string=ch,
            code=ord(ch),
            u_code=f"U+{ord(ch):04X}",
            name=unicodedata.name(ch),
            category=unicodedata.category(ch),
            combining=unicodedata.combining(ch),
        )
        for ch in unicodedata.normalize("NFD", s)
    ]


def grapheme_clusters(character_list: List[Character]) -> List[GraphemeCluster]:

    grapheme_cluster_list = []

    # current cluster being built up
    base = None
    modifiers: List[Character] = []
    string = ""

    for character in character_list:
        if character.combining:
            assert base
            modifiers.append(character)
            string += character.string
        else:
            if base:
                grapheme_cluster_list.append(
                    GraphemeCluster(
                        string=unicodedata.normalize("NFC", string),
                        base=base,
                        modifiers=modifiers,
                    )
                )
                modifiers = []
            base = character
            string = character.string
    if base:
        grapheme_cluster_list.append(
            GraphemeCluster(
                string=unicodedata.normalize("NFC", string),
                base=base,
                modifiers=modifiers,
            )
        )

    return grapheme_cluster_list


def tokens(grapheme_cluster_list: List[GraphemeCluster]) -> List[Token]:

    token_list: List[Token] = []

    # current word token being built up (non-word tokens are emitted immediately)
    clusters: List[GraphemeCluster] = []
    string = ""

    for grapheme_cluster in grapheme_cluster_list:
        if grapheme_cluster.base.category[0] in "ZP":
            if clusters:
                token_list.append(WordToken(string=string, clusters=clusters))
            token_list.append(
                Token(string=grapheme_cluster.string, clusters=[grapheme_cluster])
            )
            clusters = []
            string = ""
        else:
            clusters.append(grapheme_cluster)
            string += grapheme_cluster.string

    if clusters:
        if clusters[0].base.category[0] in "ZP":
            token_list.append(Token(string=string, clusters=clusters))
        else:
            token_list.append(WordToken(string=string, clusters=clusters))

    return token_list
