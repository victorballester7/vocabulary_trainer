from itertools import count
import math
from operator import index
import random
from matplotlib.pyplot import switch_backend

from nbformat import write
from scipy import rand
import warnings
warnings.simplefilter('always')


class word:
  def __init__(self, type, eng_word, spa_word, occur):
    self.type = type
    self.eng_word = eng_word
    self.spa_word = spa_word
    self.occur = occur

  def setFreq(self, cum_freq):
    self.cum_freq = cum_freq

  def setSpaWord(self):
    S = []
    for W in self.spa_word:
      if W.find('(') != -1:
        S.append(W[:W.index('(') - 1] + W[W.index(')') + 1:])
      else:
        S.append(W)
    self.use_spa_word = S

  def wType(self):
    dict = {
        'v': "verb",
        'f': "phrasal verb",
        'p': "phrase",
        'n': "noun",
        'i': "idiom",
        'a': "adverb",
        'A': "adjective",
        'P': "preposition",
    }
    return dict.get(self.type)


file_words = "vocab.txt"
file_occur = "occurrences.txt"
Words = []


# transforms the character '1' (for example) into the number 1.
def readlines_num(file):
  L = [int(x[0]) for x in file.readlines()]
  return L


# detect whether or not the file ends with a character '\n'. Returns 1 if
# it does and 0 otherwise.
def is_new_line(file):
  file.seek(0)
  lines = len(file.readlines())
  file.seek(0)
  L = file.read()
  if lines != L.count('\n'):
    file.write('\n')


def read_data(file_words, file_occur):
  file1 = open(file_words, 'r')
  file2 = open(file_occur, 'r+')
  L1 = file1.readlines()
  L2 = readlines_num(file2)
  # check the data of "file_occur"
  if len(L1) > len(L2):
    if len(L2) == 0:
      avg = 1
    else:
      avg = math.ceil(sum(L2) / len(L2))
    is_new_line(file2)
    for i in range(0, len(L1) - len(L2)):
      file2.write(str(avg) + '\n')
      L2.append(avg)
  ###
  file1.close()
  file2.close()
  sep = ", "
  freq, S = 0, sum(L2)
  for line in L1:
    i = line.index('|', 3)  # index of they second '|'.
    trans = line[i + 2:len(line) - 1]
    # 'len(line) - 1' in order not to read the EOL character '\n'.
    X = word(line[0], line[4:i - 1], trans.split(sep), L2[len(Words)])
    # we use the 'len(Words)' counter in order not to create a new one
    freq = freq + X.occur / S
    X.setFreq(freq)
    X.setSpaWord()
    Words.append(X)


def cond_random():
  x = random.random()
  i = 0
  while 1 > 0:
    if x < Words[i].cum_freq:
      return i
    i = i + 1


def compare_strings(str1, str2):
  return str1 == str2


def upgrade_content(file_name):
  file = open(file_name, "w")
  for i in Words:
    file.write(str(i.occur) + "\n")
  file.close()


def game(file_occur):
  print("Which modality do you want to play?\n")
  print("1-Only verbs (type 'v')\n2-Only phrasal verbs (type 'F')\n3-Only phrases (type 'p')\n4-Only nouns (type 'n')\n5-Only idioms (type 'i')\n6-Only adjectives (type 'A')\n7-Only adverbs (type 'a')\n8-Only prepositions (type 'P')\n9-Any category (type '-')\n")
  c = input()
  print("Remember: Hit 'Enter' to exit the game whenever you want. Let's play!\n")
  count = 0
  Inc = []
  while(1 > 0):
    n = cond_random()
    if c == Words[n].type or c == '-':
      print(
          "\nForeign word:\t    " +
          Words[n].eng_word +
          " (" +
          Words[n].wType() +
          ")")
      guess = input("Guess spanish word: ")
      if not guess:
        if count != 0:
          print("\n###############################")
          print("Correct answers: {c}/{t}\nFrequency of success: {s:.3f}".format(
              c=count - len(Inc), t=count, s=(count - len(Inc)) / count))
          print("###############################\n")
          print("Summary of incorrect words:\n")
          for i in Inc:
            print(Words[i].eng_word + ": ", end="")
            print(*Words[i].spa_word, sep=', ')
        print("\nExiting the program.")
        exit()

      G = [compare_strings(guess, str) for str in Words[n].use_spa_word]
      if sum(G) > 0:  # check if at least there is one correct answer
        print("Correct!\n")
        if Words[n].occur > 1:
          Words[n].occur -= 1
      else:
        Inc.append(n)
        print("Incorrect. The correct answers were: ")
        print(*Words[n].spa_word, sep=', ')
        Words[n].occur += 1
      upgrade_content(file_occur)
      count += 1


read_data(file_words, file_occur)
game(file_occur)

# STILL TO DO
# - Put error conditions when opening a file
