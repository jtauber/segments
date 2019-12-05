from typing import List

from dclasses import GraphemeCluster, Syllable, WordToken

# NOTE: some of this is just a basic port from greek-accentuation and could
# probably be made cleaner. For example, tests for "vowelness" could actually
# belong on GraphemeCluster.


def is_vowel(cluster: GraphemeCluster) -> bool:
    return cluster.bsl in "αεηιουω"


def is_diphthong(cluster1: GraphemeCluster, cluster2: GraphemeCluster) -> bool:
    return cluster1.bsl + cluster2.bsl in [
        "αι",
        "ει",
        "οι",
        "υι",
        "αυ",
        "ευ",
        "ου",
        "ηυ",
    ] and not has_diaeresis(cluster2)


def has_diaeresis(cluster: GraphemeCluster) -> bool:
    return False  # TODO: for now


def is_valid_consonant_cluster(
    cluster: GraphemeCluster, existing_onset: List[GraphemeCluster]
) -> bool:
    s = cluster.bsl + ("".join(cl.bsl for cl in existing_onset)).lower()
    return s.startswith(
        (
            "βδ",
            "βλ",
            "βρ",
            "γλ",
            "γν",
            "γρ",
            "δρ",
            "θλ",
            "θν",
            "θρ",
            "κλ",
            "κν",
            "κρ",
            "κτ",
            "μν",
            "πλ",
            "πν",
            "πρ",
            "πτ",
            "σβ",
            "σθ",
            "σκ",
            "σμ",
            "σπ",
            "στ",
            "σφ",
            "σχ",
            "στρ",
            "τρ",
            "φθ",
            "φλ",
            "φρ",
            "χλ",
            "χρ",
        )
    )


def syllabify(word_token: WordToken, DEBUG: bool = False) -> List[Syllable]:
    def debug():
        print()
        print("syllables so far:", [syl.string for syl in result])
        print(
            "current syllable being built up:",
            string,
            [cl.string for cl in current_onset],
            [cl.string for cl in current_nucleus],
            [cl.string for cl in current_coda],
        )
        print("state:", state, "cluster:", cluster.string)

    if DEBUG:
        print("syllabifying:", word_token.string)

    state = 0
    result: List[Syllable] = []

    current_coda: List[GraphemeCluster] = []
    current_nucleus: List[GraphemeCluster] = []
    current_onset: List[GraphemeCluster] = []
    string = ""

    for cluster in word_token.clusters[::-1]:
        if DEBUG:
            debug()
        if state == 0:
            if is_vowel(cluster):
                state = 1
                current_nucleus.insert(0, cluster)
            else:
                current_coda.insert(0, cluster)
            string = cluster.string + string
        elif state == 1:
            if is_vowel(cluster):
                if len(current_nucleus) == 1 and is_diphthong(
                    cluster, current_nucleus[0]
                ):
                    current_nucleus.insert(0, cluster)
                    string = cluster.string + string
                else:
                    result.insert(
                        0,
                        Syllable(
                            string=string,
                            onset=current_onset,
                            nucleus=current_nucleus,
                            coda=current_coda,
                        ),
                    )
                    current_coda = []
                    current_nucleus = [cluster]
                    current_onset = []
                    string = cluster.string
            else:
                current_onset.insert(0, cluster)
                string = cluster.string + string
                state = 2
        elif state == 2:
            if is_vowel(cluster):
                result.insert(
                    0,
                    Syllable(
                        string=string,
                        onset=current_onset,
                        nucleus=current_nucleus,
                        coda=current_coda,
                    ),
                )
                current_coda = []
                current_nucleus = [cluster]
                current_onset = []
                string = cluster.string
                state = 1
            else:
                if is_valid_consonant_cluster(cluster, current_onset):
                    current_onset.insert(0, cluster)
                    string = cluster.string + string
                else:
                    result.insert(
                        0,
                        Syllable(
                            string=string,
                            onset=current_onset,
                            nucleus=current_nucleus,
                            coda=current_coda,
                        ),
                    )
                    current_coda = [cluster]
                    current_nucleus = []
                    current_onset = []
                    string = cluster.string
                    state = 0
    result.insert(
        0,
        Syllable(
            string=string,
            onset=current_onset,
            nucleus=current_nucleus,
            coda=current_coda,
        ),
    )

    if DEBUG:
        debug()

    return result
