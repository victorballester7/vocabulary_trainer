# sets the language of the game
import random
import sys
from FileHandling import upgrade_content
from misc import *
from vars import *


def pre_game():
  print("Welcome to the Vocabulary Trainer!")
  print("This program will help you to learn new words.")
  print("Which language do you want to learn?")
  print("1. English")
  print("2. French")
  try: 
    i = int(input("Select a number: "))
  except ValueError:
    print("Please, enter a number.")
    return 1
  if i == 1:
    file_words = "data/en/vocab.txt"
    file_occur = "data/fr/occurrences.txt"
    file_incor = "data/en/incorrect.txt"
    return "en"
  elif i == 2:
    file_words = "data/fr/vocab.txt"
    file_occur = "data/fr/occurrences.txt"
    file_incor = "data/fr/incorrect.txt"
    return "fr"
  else:
    print("Please, enter a valid number.")
    game_exit(0)
  

# performs the comparison between the answered word and the correct word
def guess_word(n: int, file_occur: str, count: int, t: str):
  if t == "b":
    s = random.choice(["sf", "fs"]) # sf = spanish to foreign, fs = foreign to spanish
  else:
    s = t
  r = s[::-1] # s[::-1] revert the order of the string t. That is: 'fs' --> 'sf' and 'sf' --> 'fs'.
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

# game function for finishing the game
def game_exit(count: int):  
  if len(Inc) > 0:
    with open(file_incor, "w") as file:
      for i in Inc:
        file.write(str(i) + "\n")
  if count != 0:
    print("\n\n###############################")
    print("Correct answers: {c}/{t}\nFrequency of success: {s:.3f}".format(c=count - len(Inc), t=count, s=(count - len(Inc)) / count))
    print("###############################\n")
    if len(Inc) > 0:
      print("Summary of incorrect words:\n")
      for i in Inc:
        print(*Words[i].foreign_word, sep=", ", end=": ")
        print(*Words[i].spa_word, sep=", ")
  print("\nExiting the program.")
  sys.exit(0)

# the game
def game(file_occur: str, file_incor: str):  
  print("Which game do you want to play?\n")
  print("1- Spanish -> {c} (type 'sf')\n2- {c} -> Spanish (type 'fs')\n3- Both types (type 'b')\n".format(c=language()))
  try:
    t = input()
  except KeyboardInterrupt:
    game_exit(0)
    return
  if t not in ["sf", "fs", "b"]:
    print("Error entering the data.")
    game_exit(0)
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
    print("{0}- Only {s}s (type '{c}')".format(i + 1, s=dict.get(k), c=k))
  print("{0}- Any type of word (type '-')".format(len(dict) + 1))
  try:
    c = input()
  except KeyboardInterrupt:
    game_exit(count)
    return
  if c not in dict.keys() and c != "-":
    print("Error entering the data.")
    game_exit(count)
  print("Remember: 'Ctrl + C' to exit the game whenever you want. Let's play!\n")
  while True:
    n = cond_random()
    if c == Words[n].type or c == "-":
      guess_word(n, file_occur, count, t)
      count += 1