# transforms the character '1' (for example) into the number 1.
import math
from typing import TextIO
from vars import *
from misc import *
from Word import word

# reads the file "file_occur" and returns a list of integers corresponding
# to the data in the file


def readlines_as_numbers(file: TextIO):
    L = [int(x) for x in file.readlines()]
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

# returns the file name of the file with the words


def getFileWords(lang: str):
    return "data/{l}/vocab.txt".format(l=lang)

# returns the file name of the file with the incorrect words


def getFileIncor(lang: str, user: str):
    return "data/{l}/{u}/".format(l=lang, u=user) + incorrect_file

# returns the file name of the file with the occurrences of the words


def getFileOccur(lang: str, user: str):
    return "data/{l}/{u}/".format(l=lang, u=user) + occurrences_file

# reads the data from the files "file_words" and "file_occur"


def read_data(lang: str, user: str, Words: list[word], Inc: list[int]):
    with open(getFileWords(lang), "r") as file1:
        L1 = file1.readlines()
    with open(getFileOccur(lang, user), "r+") as file2:
        L2 = readlines_as_numbers(file2)
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
            print("Problem reading the word {s}.".format(s=X.foreign_word))
            game_exit(0, lang, user, Words, Inc)
        Words.append(X)


# upgrade the content in "file_occur"
def upgrade_content(lang: str, user: str, Words: list[word]):
    with open(getFileOccur(lang, user), "w") as file:
        for i in Words:
            file.write(str(i.occur) + "\n")


# game function for finishing the game


def game_exit(count: int, lang: str, user: str, Words: list[word], Inc: list[int]):
    if len(Inc) > 0:
        with open(getFileIncor(lang, user), "w") as file:
            for i in Inc:
                file.write(str(i) + "\n")
    if count != 0:
        print(f"{bcolors.OKGREEN}\n\n###############################")
        print("Correct answers: {c}/{t}\nFrequency of success: {s:.3f}".format(
            c=count - len(Inc), t=count, s=(count - len(Inc)) / count))
        print(f"###############################\n{bcolors.ENDC}")
        if len(Inc) > 0:
            print(f"{bcolors.FAIL}Summary of incorrect words:{bcolors.ENDC}\n")
            for i in Inc:
                print(*Words[i].foreign_word, sep=", ", end=": ")
                print(*Words[i].spa_word, sep=", ")
    print(f"{bcolors.WARNING}\nExiting the program.{bcolors.ENDC}")
    sys.exit(0)
