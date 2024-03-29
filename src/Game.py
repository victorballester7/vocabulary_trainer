# sets the language of the game
import random
from FileHandling import *
from misc import *
import os


def pre_game():
    print("Welcome to the Vocabulary Trainer!")
    print("This program will help you to learn new words.\n")
    print("Current sessions stored:")
    data_dir = "data/"
    aux_dir = data_dir + "en/"
    current_users = os.listdir(aux_dir)
    L = [current_users[i] for i in range(
        len(current_users)) if os.path.isdir(aux_dir + current_users[i])]
    for count, i in enumerate(L):
        if os.path.isdir(aux_dir + i):
            print(f"{count+1}. {i}")
        else:
            count -= 1

    print("Enter your username (press enter to use the default profile): ", end="")
    username = ""
    while True:
        try:
            username = input()
            if username == "":
                username = "default"
            else:
                try:
                    usr = int(username)
                    L = os.listdir(aux_dir)
                    if usr not in range(1, len(L) + 1):
                        print(
                            f"{bcolors.FAIL}Please, enter a valid number.{bcolors.ENDC}")
                        continue
                    username = L[usr - 1]
                except ValueError:
                    pass
            break
        except KeyboardInterrupt:
            game_exit(0, "", "", [], [])

    # for each subfolder in "data" we create a folder with the name of the user
    script_dir = os.path.dirname(__file__) + "/../" + aux_dir
    print(f"{bcolors.WARNING}Checking if user '{username}' exists...{bcolors.ENDC}")
    if os.path.isdir(script_dir + username):
        print(f"{bcolors.OKGREEN}User found!\n{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}User not found! Creating a new one...\n{bcolors.ENDC}")
        for i in os.listdir(data_dir):
            os.mkdir(data_dir + i + "/" + username)
            # create files in the new folder
            with open(data_dir + i + "/" + username + "/" + incorrect_file, "w") as file:
                pass
            with open(data_dir + i + "/" + username + "/" + occurrences_file, "w") as file:
                pass

    print("Which language do you want to learn?\n")
    for i, k in enumerate(lang_dict.keys()):
        print("{0}. {s}".format(i + 1, s=lang_dict.get(k)))
    print("\n")
    while (True):
        i = 0
        try:
            i = int(input("Select a number: "))
            if i != 1 and i != 2:
                print("Please, enter a valid number.")
                continue
        except KeyboardInterrupt:
            game_exit(0, "", username, [], [])
        except ValueError:
            print("Please, enter a number.".format())
            continue
        lang = "NOT DEFINED"
        S = list(lang_dict.keys())
        lang = S[i - 1]
        return username, lang


# performs the comparison between the answered word and the correct word
def guess_word(n: int, lang: str, user: str, count: int, t: str, Words: list[word], Inc: list[int]):
    if t == "b":
        # sf = spanish to foreign, fs = foreign to spanish
        s = random.choice(["sf", "fs"])
    else:
        s = t
    # s[::-1] revert the order of the string t. That is: 'fs' --> 'sf' and
    # 'sf' --> 'fs'.
    r = s[::-1]
    print("\nWord number {0}\n".format(count+1), end="")
    print("{c} word:\t\t\t".format(c=text_format(s, lang)), end="")
    print(*choice(n, s, Words)[0], sep=", ", end=" ")
    print("({0})".format(Words[n].wType()))
    try:
        if s == "sf":
            nWords = min([i.count(" ") for i in Words[n].use_foreign_word]) + 1
            j = 0
            while (Words[n].use_foreign_word[j].count(" ") > nWords - 1):
                j += 1
            first_char = Words[n].use_foreign_word[j][0]
        else:
            nWords = min([i.count(" ") for i in Words[n].use_spa_word]) + 1
            j = 0
            while (Words[n].use_spa_word[j].count(" ") > nWords - 1):
                j += 1
            first_char = Words[n].use_spa_word[j][0]
        guess = input(
            "Guess {c} word ({c1} word/s):\t{c2}".format(
                c=text_format(r, lang).lower(), c1=nWords, c2=first_char
            )
        )  # .lower() is to lowercase the word
        Guess = [first_char + guess, guess]
    except KeyboardInterrupt:
        game_exit(count, lang, user, Words, Inc)
        return
    G = [
        compare_strings(Guess[0], str) +
        compare_strings(Guess[1], str)
        for str in choice(n, r, Words)[1]
    ]
    if sum(G) > 0:  # check if at least there is one correct answer
        print(f"{bcolors.OKGREEN}Correct!\n{bcolors.ENDC}")
        if Words[n].occur > 0:
            Words[n].occur -= 1
    else:
        if Inc.count(n) == 0:
            Inc.append(n)

        L = choice(n, r, Words)[1]
        if len(L) == 1:
            print(f"{bcolors.FAIL}Incorrect. The correct answer was: {bcolors.ENDC}")
        else:
            print(
                f"{bcolors.FAIL}Incorrect. The correct answers were: {bcolors.ENDC}")
        print(*choice(n, r, Words)[1], sep=", ")
        Words[n].occur += 1
    upgrade_content(lang, user, Words)

# the game


def game(lang: str, user: str, Words: list[word], Inc: list[int]):
    print("Which game do you want to play?\n")
    print(
        "1. Spanish -> {c}\n2. {c} -> Spanish\n3. Both types\n".format(c=lang_dict[lang]))

    while (True):
        try:
            t = int(input())
            if t != 1 and t != 2 and t != 3:
                print("Please, enter a valid number.")
                continue
        except KeyboardInterrupt:
            game_exit(0, lang, user, Words, Inc)
            return
        except ValueError:
            print("Please, enter a number.".format())
            continue
        if t == 1:
            t = "sf"
        elif t == 2:
            t = "fs"
        else:  # t == 3:
            t = "b"
        break
    count = 0
    with open(getFileIncor(lang, user), "r") as file:
        for i in file.readlines():
            if count == 0:
                print("Review of last day's game:\n")
            guess_word(int(i), lang, user, count, t, Words, Inc)
            count += 1
            if count == len(file.readline()):
                print("\n")
    print("Which modality do you want to play?\n")
    for i, k in enumerate(dict.keys()):
        print("{0}. Only {s}s".format(i + 1, s=dict.get(k)))
    print("{0}. Any type of word".format(len(dict) + 1))
    while (True):
        try:
            c = int(input())
            if c not in range(1, len(dict) + 2):
                print("Please, enter a valid number.")
                continue
        except KeyboardInterrupt:
            game_exit(0, lang, user, Words, Inc)
            return
        except ValueError:
            print("Please, enter a number.".format())
            continue
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
        else:  # if c == 8:
            c = "-"
        break
    print("Remember: 'Ctrl + C' to exit the game whenever you want. Let's play!\n")
    count_rep = 0
    while count_rep < 10*len(Words):
        n = cond_random(Words)
        if c == Words[n].type or c == "-":
            guess_word(n, lang, user, count, t, Words, Inc)
            count += 1
            count_rep = 0
        else:
            count_rep += 1
    print("There are no words of the type '{0}'.".format(c))
    game_exit(count, lang, user, Words, Inc)
