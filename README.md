# Python program to practice vocabulary from a foreign language.

## Description

This program is a simple vocabulary trainer. It reads a list of words from a file and asks the user to translate them. If the user enters the correct translation, the program will ask the next word. If the user enters an incorrect translation, the program will save the incorrect word and ask the user to translate it again in at the beginning of the next session.

The program is designed for a Spanish speaker to practice foreign languages.
Current languages implemented:

- English
- French

## Requirements

- Python 3

## Installation and usage

Clone the repository and run the program with Python 3.

```
git clone git@github.com:victorballester7/vocabulary_trainer.git
cd vocabulary_trainer
chmod +x run.sh
./run.sh
```

## Personalization

You can add more words to the vocabulary by editing the `vocab.txt` file inside the corresponding language folder in the `data` folder. For that, you should use the following syntax:

```
type | word_1_1 (extra_info_1_1) word_1_2 (extra_info_1_2) ... word_1_n (extra_info_1_n1), word_2_1 (extra_info_2_1) word_2_2 (extra_info_2_2) ... word_2_n2 (extra_info_2_n3), ..., word_m_1 (extra_info_m_1) word_m_2 (extra_info_m_2) ... word_m_nm (extra_info_m_nm) | trans_word_1_1 (extra_info_1_1) trans_word_1_2 (extra_info_1_2) ...  trans_word_1_r1 (extra_info_1_r1), trans_word_2_1 (extra_info_2_1) trans_word_2_2 (extra_info_2_2) ... trans_word_2_r2 (extra_info_2_r2), ..., trans_word_s_1 (extra_info_s_1) trans_word_s_2 (extra_info_s_2) ... trans_word_s_rs (extra_info_s_rs)
```

where `type` is one of the following: `noun`, `verb`, `adje`, `adve`, `ph-v`, `expr` or `prep` and correspond respectively to noun, verb, adjective, adverb, phrasal verb, expression and preposition; `word_i_j` is the `j`-th word of the set `i`. `trans_word_i_j` is the `j`-th word of the translation set `i`, and `extra_info_i_j` is any extra information that you may want to add to the `j`-th word in order to help you to remember the word, but will not be affected by the program, i.e. you won't be asked to write it to get the word right.

An important thing to note you should not use commas (`,`) or pipes (`|`) inside the words or the extra information, as they are used to separate the different words and the different sets of words.

Here are some examples:

```
noun | fitness | forma física
ph-v | fall out (with sb) | enfadarse con, enfadarse
verb | submit | enviar, presentar (un documento / un plan...)
ph-v | get through (sth) (survive) | terminar, acabar, superar
ph-v | fill in (sth), fill (sth) in | rellenar, completar (un formulario...)
```

## Contributing

If you want to contribute to this project adding more languages or improving the code, feel free to open a pull request.
