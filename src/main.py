from Game import game, pre_game
from FileHandling import read_data
from vars import *
from Word import word

Words: list[word] = []  # list of words
Inc: list[int] = []  # list of incorrect words

user, lang = pre_game()  # type: ignore
read_data(lang, user, Words, Inc)
game(lang, user, Words, Inc)
