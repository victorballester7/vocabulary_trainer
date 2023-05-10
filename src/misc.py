
# random integer number conditioned to the number in "Words[i].occur"
import random
import sys
from vars import *
from Word import word
# I put this here (and not in vars.py) because if I put it in vars.py, it
# would result in a circular import.


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cond_random(Words: list[word]):
    x = random.random()
    i = 0
    while 1 > 0:
        if x <= Words[i].cum_freq:
            return i
        i = i + 1
    return 0


# compares two strings
def compare_strings(str1: str, str2: str):
    return str1 == str2


def language(lang: str):
    if lang == "en":
        return "English"
    else:  # lang == "fr":
        return "French"


def text_format(t: str, lang: str):
    if t == "fs":  # foreign to spanish
        if lang == "en":
            return "English"
        elif lang == "fr":
            return "French"
        else:
            return "NOT DEFINED"
    else:  # t == "sf":  # spanish to foreign
        return "Spanish"


def choice(n: int, t: str, Words: list[word]):
    if t == "fs":
        return [Words[n].foreign_word, Words[n].use_foreign_word]
    else:
        return [Words[n].spa_word, Words[n].use_spa_word]
