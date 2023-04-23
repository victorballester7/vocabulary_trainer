
# random integer number conditioned to the number in "Words[i].occur"
import random
from vars import *

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
  else: # lang == "fr":
    return "French"
  
def text_format(t: str):
  if t == "ef":
    if lang == "en":
      return "English"
    else: # lang == "fr":
      return "French"
  else:
    return "Spanish"


def choice(n: int, t: str):
  if t == "fs":
    return [Words[n].foreign_word, Words[n].use_foreign_word]
  else:
    return [Words[n].spa_word, Words[n].use_spa_word]