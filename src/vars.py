sep = ", "  # separator for the words
# bound for the number of occurrences from which the word is NOT included
# in the game (because the player has already learned it)
BOUND = -3
DEFAULT_PROFILE = "default"
incorrect_file = "incorrect.txt"
occurrences_file = "occurrences.txt"

lang_dict = {
    "en": "English",
    "fr": "French",
}

dict = {  # all keys must have the same length
    "verb": "verb",
    "ph-v": "phrasal verb",
    "noun": "noun",
    "expr": "expression",
    "adve": "adverb",
    "adje": "adjective",
    "prep": "preposition",
}
