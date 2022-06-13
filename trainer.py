import math
import random
from typing import TextIO
import sys


class word:
  def __init__(self, type: str,
               eng_word: list[str], spa_word: list[str], occur: int):
    self.type = type
    self.eng_word = eng_word
    self.spa_word = spa_word
    self.occur = occur

  def setFreq(self, cum_freq: float):
    self.cum_freq = cum_freq

  def setSpaWord(self):
    S: list[str] = []
    for w in self.spa_word:
      while w.count("(") > 0:
        if w.index("(") == 0:
          return 1
        try:
          w = w[: w.index("(") - 1] + w[w.index(")") + 1:]
        except ValueError:
          return 1
      S.append(w)
    self.use_spa_word = S

  def setEngWord(self):
    S: list[str] = []
    for w in self.eng_word:
      while w.count("(") > 0:
        if w.index("(") == 0:
          return 1
        try:
          w = w[: w.index("(") - 1] + w[w.index(")") + 1:]
        except ValueError:
          return 1
      S.append(w)
    self.use_eng_word = S

  def wType(self):
    return dict.get(self.type)


file_words = "vocab.txt"
file_occur = "occurrences.txt"
file_incor = "incorrect.txt"
Words: list[word] = []
Inc: list[int] = []
sep = ", "
BOUND = -3
dict = {  # all keys must have the same length
    "verb": "verb",
    "ph-v": "phrasal verb",
    "noun": "noun",
    "expr": "expression",
    "adve": "adverb",
    "adje": "adjective",
    "prep": "preposition",
}


# transforms the character '1' (for example) into the number 1.
def readlines_num(file: TextIO):
  L = [int(x[0]) for x in file.readlines()]
  return L


# detect whether or not the file ends with a character '\n'. If it does,
# the file remains the same. It not, '\n' is added at the EOL.
def is_new_line(file: TextIO):
  file.seek(0)
  lines = len(file.readlines())
  file.seek(0)
  L = file.read()
  if lines != L.count("\n"):
    file.write("\n")


# reads the data from the files "file_words" and "file_occur"
def read_data(file_words: str, file_occur: str):
  with open(file_words, "r") as file1:
    L1 = file1.readlines()
  with open(file_occur, "r+") as file2:
    L2 = readlines_num(file2)
    # check the data of "file_occur"
    if len(L1) > len(L2):
      if len(L2) == 0:
        avg = 1
      else:
        avg = math.ceil(sum(L2) / len(L2))
      is_new_line(file2)
      for i in range(0, len(L1) - len(L2)):
        file2.write(str(avg) + "\n")
        L2.append(avg)
  freq, S, wlen = 0, sum(L2), len(list(dict.keys())[0])
  for line in L1:
    if L2[len(Words)] <= BOUND:
      continue
    i = line.index("|", wlen + 2)  # index of they second '|'.
    type = line[:4]
    eng = line[wlen + 3: i - 1]
    esp = line[i + 2: len(line) - 1]
    # 'len(line) - 1' in order not to read the EOL character '\n'.
    X = word(type, eng.split(sep), esp.split(sep), L2[len(Words)])
    # we use the 'len(Words)' counter in order not to create a new one
    freq = freq + X.occur / S
    X.setFreq(freq)
    if X.setEngWord() == 1 or X.setSpaWord() == 1:
      print("Problem reading the word {s}.".format(s=X.eng_word))
      game_exit(0)
    Words.append(X)


# random integer number conditioned to the number in "Words[i].occur"
def cond_random():
  x = random.random()
  i = 0
  while 1 > 0:
    if x < Words[i].cum_freq:
      return i
    i = i + 1
  return 0


def compare_strings(str1: str, str2: str):  # compares two strings
  return str1 == str2


def upgrade_content(file_name: str):  # upgrade the content in "file_occur"
  with open(file_name, "w") as file:
    for i in Words:
      file.write(str(i.occur) + "\n")


def text_format(t: str):
  if t == "es":
    return "English"
  else:
    return "Spanish"


def choice(n: int, t: str):
  if t == "es":
    return [Words[n].eng_word, Words[n].use_eng_word]
  else:
    return [Words[n].spa_word, Words[n].use_spa_word]


# performs the comparison between the answered word and the correct word
def guess_word(n: int, file_occur: str, count: int, t: str):
  if t == "b":
    s = random.choice(["se", "es"])
  else:
    s = t
  # s[::-1] revert the order of the string t. That is: 'es' --> 'se'
  # and 'se' --> 'es'.
  r = s[::-1]
  print("\n{c} word:\t\t         ".format(c=text_format(s)), end="")
  print(*choice(n, s)[0], sep=", ", end=" ")
  print("({0})".format(Words[n].wType()))
  try:
    if s == "se":
      first_char = Words[n].eng_word[0][0]
      nWords = min([i.count(" ") for i in Words[n].use_eng_word]) + 1
      guess = input(
          "Guess {c} word ({c1} word/s):   {c2}".format(
              c=text_format(r).lower(), c1=nWords, c2=first_char
          )
      )  # .lower() is to lowercase the word
      guess = first_char + guess
    else:
      guess = input(
          "Guess {c} word:\t         ".format(
              c=text_format(r).lower()))
  except KeyboardInterrupt:
    game_exit(count)
  G = [compare_strings(guess, str) for str in choice(n, r)[1]]
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


def game_exit(count: int):  # game function for finishing the game
  if len(Inc) > 0:
    with open(file_incor, "w") as file:
      for i in Inc:
        file.write(str(i) + "\n")
  if count != 0:
    print("\n\n###############################")
    print(
        "Correct answers: {c}/{t}\nFrequency of success: {s:.3f}".format(
            c=count - len(Inc), t=count, s=(count - len(Inc)) / count
        )
    )
    print("###############################\n")
    if len(Inc) > 0:
      print("Summary of incorrect words:\n")
      for i in Inc:
        print(*Words[i].eng_word, sep=", ", end=": ")
        print(*Words[i].spa_word, sep=", ")
  print("\nExiting the program.")
  sys.exit(0)


def game(file_occur: str, file_incor: str):  # the game
  print("Which game do you want to play?\n")
  print(
      "1- Spanish -> English (type 'se')\n2- English -> Spanish (type 'es')\n3- Both types (type 'b')\n"
  )
  try:
    t = input()
  except KeyboardInterrupt:
    game_exit(0)
  if t not in ["se", "es", "b"]:
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
  if c not in dict.keys() and c != "-":
    print("Error entering the data.")
    game_exit(count)
  print("Remember: 'Ctrl + C' to exit the game whenever you want. Let's play!\n")
  while True:
    n = cond_random()
    if c == Words[n].type or c == "-":
      guess_word(n, file_occur, count, t)
      count += 1


read_data(file_words, file_occur)
game(file_occur, file_incor)
