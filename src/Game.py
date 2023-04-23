# sets the language of the game
import random
from FileHandling import upgrade_content
from misc import *
import vars


def pre_game():
  print("Welcome to the Vocabulary Trainer!")
  print("This program will help you to learn new words.")
  print("Which language do you want to learn?")
  print("1. English")
  print("2. French")
  try:
    i = int(input("Select a number: "))
  except ValueError:
    print("Please, enter a number.".format())
    game_exit(0)
    return
  if i == 1:
    return "en", "data/en/vocab.txt", "data/en/occurrences.txt", "data/en/incorrect.txt"
  elif i == 2:
    return "fr", "data/fr/vocab.txt", "data/fr/occurrences.txt", "data/fr/incorrect.txt"
  else:
    print("Please, enter a valid number.")
    game_exit(0)
    return


# performs the comparison between the answered word and the correct word
def guess_word(n: int, file_occur: str, count: int, t: str):
  if t == "b":
    # sf = spanish to foreign, fs = foreign to spanish
    s = random.choice(["sf", "fs"])
  else:
    s = t
  # s[::-1] revert the order of the string t. That is: 'fs' --> 'sf' and
  # 'sf' --> 'fs'.
  r = s[::-1]
  print("\n{c} word:\t\t         ".format(c=text_format(s)), end="")
  print(*choice(n, s)[0], sep=", ", end=" ")
  print("({0})".format(Words[n].wType()))
  try:
    if s == "sf":
      first_char = Words[n].foreign_word[0][0]
      nWords = min([i.count(" ") for i in Words[n].use_foreign_word]) + 1
    else:
      first_char = Words[n].spa_word[0][0]
      nWords = min([i.count(" ") for i in Words[n].use_spa_word]) + 1
    guess = input(
        "Guess {c} word ({c1} word/s):   {c2}".format(
            c=text_format(r).lower(), c1=nWords, c2=first_char
        )
    )  # .lower() is to lowercase the word
    Guess = [first_char + guess, guess]
  except KeyboardInterrupt:
    game_exit(count)
    return
  G = [
      compare_strings(Guess[0], str) +
      compare_strings(Guess[1], str)
      for str in choice(n, r)[1]
  ]
  if sum(G) > 0:  # check if at least there is one correct answer
    print("Correct!\n")
    Words[n].occur -= 1
  else:
    if Inc.count(n) == 0:
      Inc.append(n)
    print("Incorrect. The correct answers were: ")
    print(*choice(n, r)[1], sep=", ")
    Words[n].occur += 1
  upgrade_content(file_occur)

# the game


def game(file_occur: str, file_incor: str):
  print("Which game do you want to play?\n")
  print(
      "1. Spanish -> {c}\n2. {c} -> Spanish\n3. Both types\n".format(c=language()))
  try:
    t = int(input())
  except KeyboardInterrupt:
    game_exit(0)
    return
  except ValueError:
    print("Please, enter a number.")
    return
  if t == 1:
    t = "sf"
  elif t == 2:
    t = "fs"
  elif t == 3:
    t = "b"
  else:
    print("Error entering the data.")
    game_exit(0)
    return
  count = 0
  with open(file_incor, "r") as file:
    for i in file.readlines():
      if count == 0:
        print("Review of last day's game:\n")
      guess_word(int(i), file_occur, count, t)
      count += 1
      if count == len(file.readline()):
        print("\n")
  print("Which modality do you want to play?\n")
  for i, k in enumerate(dict.keys()):
    print("{0}. Only {s}s (type '{c}')".format(i + 1, s=dict.get(k), c=k))
  print("{0}. Any type of word (type '-')".format(len(dict) + 1))
  try:
    c = int(input())
  except KeyboardInterrupt:
    game_exit(count)
    return
  except ValueError:
    print("Please, enter a number.")
    return
  if c == 1:
    c = "verb"
  elif c == 2:
    c = "ph-v"
  elif c == 3:
    c = "noun"
  elif c == 4:
    c = "expr"
  elif c == 5:
    c = "adve"
  elif c == 6:
    c = "adje"
  elif c == 7:
    c = "prep"
  elif c == 8:
    c = "-"
  else:
    print("Error entering the data.")
    game_exit(count)
    return
  print("Remember: 'Ctrl + C' to exit the game whenever you want. Let's play!\n")
  while True:
    n = cond_random()
    if c == Words[n].type or c == "-":
      guess_word(n, file_occur, count, t)
      count += 1
