Segments Prototype
==================

This is an idea I've had for years but finally playing around with it using dataclasses (and type annotation).

The idea is to have specific datastructures for things like characters, grapheme clusters, tokens, syllables, etc.

In some senses, this is a more object-oriented and typed alternative to things like ``greek-accentuation``.

It's still very much a work in progress and I've only just started.


    This is a literate doctest.
    Run ``python -m doctest -v README.rst`` to test.

>>> from constructors import characters, grapheme_clusters, tokens
>>> from syllabification import syllabify


Characters
----------

``characters`` takes a string and breaks it down to a list of NFD code points represented by ``Character`` instances.

Each ``Character`` has a ``string`` representation, ``code``, ``u_code``, ``name``, ``category``, and ``combining`` class on it.

>>> character_list = characters("ὁ λόγος")

>>> for character in character_list:
...     print(character)
Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0)
Character(string='̔', code=788, u_code='U+0314', name='COMBINING REVERSED COMMA ABOVE', category='Mn', combining=230)
Character(string=' ', code=32, u_code='U+0020', name='SPACE', category='Zs', combining=0)
Character(string='λ', code=955, u_code='U+03BB', name='GREEK SMALL LETTER LAMDA', category='Ll', combining=0)
Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0)
Character(string='́', code=769, u_code='U+0301', name='COMBINING ACUTE ACCENT', category='Mn', combining=230)
Character(string='γ', code=947, u_code='U+03B3', name='GREEK SMALL LETTER GAMMA', category='Ll', combining=0)
Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0)
Character(string='ς', code=962, u_code='U+03C2', name='GREEK SMALL LETTER FINAL SIGMA', category='Ll', combining=0)

Grapheme Clusters
-----------------

``grapheme_clusters`` takes a list of ``Character`` instances and groups them into a list of ``GraphemeCluster`` instances.

Each ``GraphemeCluster`` has a ``string`` representation, a ``base`` Character and a list of ``modifiers``.

>>> grapheme_cluster_list = grapheme_clusters(character_list)
>>> for grapheme_cluster in grapheme_cluster_list:
...     print(grapheme_cluster)
GraphemeCluster(string='ὁ', base=Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0), modifiers=[Character(string='̔', code=788, u_code='U+0314', name='COMBINING REVERSED COMMA ABOVE', category='Mn', combining=230)])
GraphemeCluster(string=' ', base=Character(string=' ', code=32, u_code='U+0020', name='SPACE', category='Zs', combining=0), modifiers=[])
GraphemeCluster(string='λ', base=Character(string='λ', code=955, u_code='U+03BB', name='GREEK SMALL LETTER LAMDA', category='Ll', combining=0), modifiers=[])
GraphemeCluster(string='ό', base=Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0), modifiers=[Character(string='́', code=769, u_code='U+0301', name='COMBINING ACUTE ACCENT', category='Mn', combining=230)])
GraphemeCluster(string='γ', base=Character(string='γ', code=947, u_code='U+03B3', name='GREEK SMALL LETTER GAMMA', category='Ll', combining=0), modifiers=[])
GraphemeCluster(string='ο', base=Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0), modifiers=[])
GraphemeCluster(string='ς', base=Character(string='ς', code=962, u_code='U+03C2', name='GREEK SMALL LETTER FINAL SIGMA', category='Ll', combining=0), modifiers=[])

I haven't implemented this but extracting (or adding) diacritics could now be done through methods on ``GraphemeCluster`` rather than Python string hacking.

Tokens
------

``tokens`` takes a list of ``GraphemeCluster`` instances and groups them into a list of ``Token`` instances of which ``WordToken`` is a subclass used if the token is a word.

>>> token_list = tokens(grapheme_cluster_list)
>>> for token in token_list:
...     print(type(token), [cl.string for cl in token.clusters])
<class 'dclasses.WordToken'> ['ὁ']
<class 'dclasses.Token'> [' ']
<class 'dclasses.WordToken'> ['λ', 'ό', 'γ', 'ο', 'ς']

To simplify the display above, I just show the grapheme cluster strings but they are actually full ``GraphemeCluster`` instances.

Syllabification
---------------

>>> words_to_syllabify = "γυναικός φῡ́ω καταλλάσσω γγγ ῑ́̔στην Οὐρίου ευιλατευσαι"
>>> tokens_to_syllabify = tokens(grapheme_clusters(characters(words_to_syllabify)))

>>> from dclasses import WordToken

>>> for token in tokens_to_syllabify:
...     if isinstance(token, WordToken):
...         print([syllable.string for syllable in syllabify(token)])
['γυ', 'ναι', 'κός']
['φῡ́', 'ω']
['κα', 'ταλ', 'λάσ', 'σω']
['γγγ']
['ῑ́̔', 'στην']
['Οὐ', 'ρί', 'ου']
['ε', 'υι', 'λα', 'τευ', 'σαι']

**NOTE**: the results of syllabification should be put on a dataclass instance but because the ``syllabify`` function is Greek-specific, we'd have to work out how to dispatch it properly.

``syllabify`` is actually returning a list of ``Syllable`` instances which have ``GraphemeCluster`` lists for each of ``onset``, ``nucleus``, and ``coda``:

>>> for syllable in syllabify(tokens_to_syllabify[0]):
...     print(
...         syllable.string,
...         [cluster.string for cluster in syllable.onset],
...         [cluster.string for cluster in syllable.nucleus],
...         [cluster.string for cluster in syllable.coda]
...     )
γυ ['γ'] ['υ'] []
ναι ['ν'] ['α', 'ι'] []
κός ['κ'] ['ό'] ['ς']

You can also run syllabify in DEBUG mode:

>>> syllabify(tokens_to_syllabify[0], DEBUG=True)
syllabifying: γυναικός
<BLANKLINE>
syllables so far: []
current syllable being built up:  [] [] []
state: 0 cluster: ς
<BLANKLINE>
syllables so far: []
current syllable being built up: ς [] [] ['ς']
state: 0 cluster: ό
<BLANKLINE>
syllables so far: []
current syllable being built up: ός [] ['ό'] ['ς']
state: 1 cluster: κ
<BLANKLINE>
syllables so far: []
current syllable being built up: κός ['κ'] ['ό'] ['ς']
state: 2 cluster: ι
<BLANKLINE>
syllables so far: ['κός']
current syllable being built up: ι [] ['ι'] []
state: 1 cluster: α
<BLANKLINE>
syllables so far: ['κός']
current syllable being built up: αι [] ['α', 'ι'] []
state: 1 cluster: ν
<BLANKLINE>
syllables so far: ['κός']
current syllable being built up: ναι ['ν'] ['α', 'ι'] []
state: 2 cluster: υ
<BLANKLINE>
syllables so far: ['ναι', 'κός']
current syllable being built up: υ [] ['υ'] []
state: 1 cluster: γ
<BLANKLINE>
syllables so far: ['γυ', 'ναι', 'κός']
current syllable being built up: γυ ['γ'] ['υ'] []
state: 2 cluster: γ
[Syllable(string='γυ', onset=[GraphemeCluster(string='γ', base=Character(string='γ', code=947, u_code='U+03B3', name='GREEK SMALL LETTER GAMMA', category='Ll', combining=0), modifiers=[])], nucleus=[GraphemeCluster(string='υ', base=Character(string='υ', code=965, u_code='U+03C5', name='GREEK SMALL LETTER UPSILON', category='Ll', combining=0), modifiers=[])], coda=[]), Syllable(string='ναι', onset=[GraphemeCluster(string='ν', base=Character(string='ν', code=957, u_code='U+03BD', name='GREEK SMALL LETTER NU', category='Ll', combining=0), modifiers=[])], nucleus=[GraphemeCluster(string='α', base=Character(string='α', code=945, u_code='U+03B1', name='GREEK SMALL LETTER ALPHA', category='Ll', combining=0), modifiers=[]), GraphemeCluster(string='ι', base=Character(string='ι', code=953, u_code='U+03B9', name='GREEK SMALL LETTER IOTA', category='Ll', combining=0), modifiers=[])], coda=[]), Syllable(string='κός', onset=[GraphemeCluster(string='κ', base=Character(string='κ', code=954, u_code='U+03BA', name='GREEK SMALL LETTER KAPPA', category='Ll', combining=0), modifiers=[])], nucleus=[GraphemeCluster(string='ό', base=Character(string='ο', code=959, u_code='U+03BF', name='GREEK SMALL LETTER OMICRON', category='Ll', combining=0), modifiers=[Character(string='́', code=769, u_code='U+0301', name='COMBINING ACUTE ACCENT', category='Mn', combining=230)])], coda=[GraphemeCluster(string='ς', base=Character(string='ς', code=962, u_code='U+03C2', name='GREEK SMALL LETTER FINAL SIGMA', category='Ll', combining=0), modifiers=[])])]
