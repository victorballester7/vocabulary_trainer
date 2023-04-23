from Game import game, pre_game
from FileHandling import read_data
from vars import *

lang, file_words, file_occur, file_incor = pre_game()  # type: ignore
read_data(file_words, file_occur)
game(file_occur, file_incor)
