from Word import word


Words: list[word] = [] # list of words
Inc: list[int] = [] # list of incorrect words
sep = ", " # separator for the words
BOUND = -3 # bound for the number of occurrences from which the word is NOT included in the game (because the player has already learned it)
dict = {  # all keys must have the same length
    "verb": "verb",
    "ph-v": "phrasal verb",
    "noun": "noun",
    "expr": "expression",
    "adve": "adverb",
    "adje": "adjective",
    "prep": "preposition",
}
lang = "" # language of the game
file_words = "" # file with the words
file_occur = "" # file with the occurrences of each word
file_incor = "" # file with the incorrect words