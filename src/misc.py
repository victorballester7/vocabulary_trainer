
# random integer number conditioned to the number in "Words[i].occur"
import random
import sys
from vars import *
from Word import word
# I put this here (and not in vars.py) because if I put it in vars.py, it
# would result in a circular import.
Words: list[word] = []  # list of words
Inc: list[int] = []  # list of incorrect words


def cond_random():
  x = random.random()
  i = 0
  while 1 > 0:
    if x < Words[i].cum_freq:
      return i
    i = i + 1
  return 0


# compares two strings
def compare_strings(str1: str, str2: str):
  return str1 == str2


def language():
  if lang == "en":
    return "English"
  else:  # lang == "fr":
    return "French"


def text_format(t: str):
  if t == "fs":
    if lang == "en":
      return "English"
    else:  # lang == "fr":
      return "French"
  else:
    return "Spanish"


def choice(n: int, t: str):
  if t == "fs":
    return [Words[n].foreign_word, Words[n].use_foreign_word]
  else:
    return [Words[n].spa_word, Words[n].use_spa_word]

# game function for finishing the game


def game_exit(count: int):
  if len(Inc) > 0:
    with open(file_incor, "w") as file:
      for i in Inc:
        file.write(str(i) + "\n")
  if count != 0:
    print("\n\n###############################")
    print("Correct answers: {c}/{t}\nFrequency of success: {s:.3f}".format(
        c=count - len(Inc), t=count, s=(count - len(Inc)) / count))
    print("###############################\n")
    if len(Inc) > 0:
      print("Summary of incorrect words:\n")
      for i in Inc:
        print(*Words[i].foreign_word, sep=", ", end=": ")
        print(*Words[i].spa_word, sep=", ")
  print("\nExiting the program.")
  sys.exit(0)
