#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_LEN 100

typedef struct {
  int num;              // label associated to that word
  int occur;            // probability
  double cum_freq;      // cumulative frequency
  char *foreign_word;   // foreign word
  char type;            // type of word. Possible options: verb (v), noun (n), idiom (i), adjective (A), adverb (a).
  int Ntrans;           // number of translations
  char **spanish_word;  // translation
} word;

int line_counter(char *);
int check_data(char *, int);
int is_substr_eq(char *, char *, int);
int char_occur(char *, char *);
char *strcatchar(char *, char);
char *strpop(char *);
char **sep_str(char *, char *);
int read_data(char *, char *, int, word *);
void cum_freq(int, word *);
void upgrade_content(char *, int, word *);
double rand_double(double, double);
int cond_rand_ind(int, word *);
int str_comp(char *, char **, int);
void game(char *, int, word *, char);
char game_mod(word *);
char *part_of_speech(char);

int main() {
  char file_words[11] = "vocab.txt", file_occur[16] = "occurrences.txt";
  int n = line_counter(file_words), x;
  if (n == 0) {
    printf("There is no file called '%s' or there are no words inside it.\n", file_words);
    return 1;
  }
  word vocab[n];
  if (read_data(file_words, file_occur, n, vocab) == 1) {
    printf("Problem reading the data.\n");
    return 1;
  }

  srand(time(0));  // to generate different random numbers on the same execution.
  char c = game_mod(vocab);
  if (c == '1') {
    printf("Error.\n");
    return 1;
  }
  game(file_occur, n, vocab, c);
  // printf("What do you want to do?\n1- English -> Spanish\n2- Spanish -> English");
  // scanf("%i", &x);
  // switch (n) {
  //   case 1:
  //   case 2:
  //   default:
  //     printf("Error! You shall introduce either 1 or 2.\n");
  //     return 1;
  // }
  free(vocab->foreign_word);
  free(vocab->spanish_word);
  return 0;
}

int line_counter(char *file) {  // counter of line in a file.
  FILE *doc;
  int c = '\0', pc = '\n';
  int linies = 0;

  doc = fopen(file, "r");
  if (doc == NULL)
    return 0;
  while (c = fgetc(doc), c != EOF) {
    if (c == '\n' && pc != '\n')
      linies++;
    pc = c;
  }
  if (pc != '\n')  // Sometimes we do not click "intro" in the last line of the file.
    linies++;
  fclose(doc);
  return linies;
}

int check_data(char *file_occur, int Numlines) {  // check whether the data in the file "occurrences.txt" is correct or not.
  FILE *file;
  file = fopen(file_occur, "a+");
  int x, sum = 0, k = 0;  // k = line counter
  if (file == NULL)
    return 1;
  while ((fscanf(file, "%i\n", &x) != EOF)) {  // assignments of words and occurrences to each word at the same time (same bucle).
    sum += x;
    if (x <= 0)
      return 1;
    k++;
  }
  int avg = sum / Numlines + 1;  // sum / Numlines + 1 = ceil(sum / Numlines).
  for (int i = 0; i < Numlines - k; i++)
    fprintf(file, "%i\n", avg);  // we assign the average of the current occurrences to each new word.
  fclose(file);
  return 0;
}

int is_substr_eq(char *str, char *c, int j) {  // check whether or not the string "str" contains the substrig "c" starting at position "j".
  for (int k = 0; k < strlen(c); k++) {
    if (str[j + k] != c[k])
      return 1;
  }
  return 0;
}

int char_occur(char *str, char *c) {  // count the occurrences of "c" along "str".
  int count = 0;
  for (int j = 0; j < strlen(str); j++) {
    if (is_substr_eq(str, c, j) == 0)
      count++;
  }
  return count;
}

char *strcatchar(char *dest, char src) {  // add a char to a string.
  char c[2];
  c[0] = src;
  c[1] = '\0';
  return strcat(dest, c);  // c must be a string (i.e. must end with the character '\0').
}

char *strpop(char *str) {  // delete last character of a string.
  str[strlen(str) - 1] = '\0';
  return str;
}

char **sep_str(char *str, char *del) {  // separate the string "str" into multiple substrings delimited by the subtring "del" in "str".
  char **part_str, aux[strlen(str)];    // token and partitioned string (array of strings).
  int n = char_occur(str, del), j = 0;
  part_str = (char **)malloc((n + 1) * sizeof(char *));
  if ((part_str[j] = (char *)malloc(strlen(str) * sizeof(char))) == NULL)
    return NULL;
  for (int i = 0; i < strlen(str); i++) {
    if (is_substr_eq(str, del, i) == 1) {
      strcatchar(part_str[j], str[i]);
    } else {
      i += strlen(del) - 1;  // -1 because at the beginning of the next bucle "i" is incremented by 1.
      j++;
      if ((part_str[j] = (char *)malloc(strlen(str) * sizeof(char))) == NULL)
        return NULL;
    }
  }
  return part_str;
}

int read_data(char *file_words, char *file_occur, int Numlines, word *vocab) {  // read all the data.
  FILE *file1, *file2;
  char spa[MAX_LEN], *token;
  char del[3] = ", ";
  file1 = fopen(file_words, "r");
  file2 = fopen(file_occur, "r");
  if (file1 == NULL || file2 == NULL || check_data(file_occur, Numlines) == 1)
    return 1;
  for (int i = 0; i < Numlines; i++) {  // memory allocation
    if ((vocab[i].foreign_word = (char *)malloc(MAX_LEN * sizeof(char))) == NULL)
      return 1;
  }
  int i = 0;
  while ((fscanf(file1, "%c | %[^|]| %[^\n]\n", &vocab[i].type, vocab[i].foreign_word, spa) != EOF) && (fscanf(file2, "%i\n", &vocab[i].occur) != EOF)) {  // assignments of words and occurrences to each word at the same time (same bucle)
    strpop(vocab[i].foreign_word);
    vocab[i].num = i;
    int j = char_occur(spa, del);
    vocab[i].Ntrans = j + 1;
    if ((vocab[i].spanish_word = sep_str(spa, del)) == NULL)  // separate the multiple translations
      return 1;
    i++;
  }
  cum_freq(Numlines, vocab);
  fclose(file1);
  fclose(file2);
  return 0;
}

void cum_freq(int Numlines, word *vocab) {  // computes the cumulative frequency of each word.
  int sum = 0;
  for (int i = 0; i < Numlines; i++) {
    sum += vocab[i].occur;
  }
  for (int i = 0; i < Numlines; i++) {
    if (i == 0)
      vocab[i].cum_freq = vocab[i].occur * 1. / sum;
    else
      vocab[i].cum_freq = vocab[i - 1].cum_freq + vocab[i].occur * 1. / sum;
  }
}

void upgrade_content(char *file_name, int Numlines, word *vocab) {  // upgrades the content in 'filename' and upgrades the cumulative frequencies of *vocab.
  FILE *file;
  file = fopen(file_name, "w");
  if (file == NULL) {
    exit(1);
  }
  for (int i = 0; i < Numlines; i++) {
    fprintf(file, "%i\n", vocab[i].occur);
  }
  cum_freq(Numlines, vocab);
  fclose(file);
}

double rand_double(double min, double max) {  // random number in the interval (min,max].
  return min + (max - min) * rand() * 1. / RAND_MAX;
}

int cond_rand_ind(int Numlines, word *vocab) {  // conditioned random integer (in terms of relative frequeces of words).
  double x = rand_double(0, 1);
  int k;
  for (k = 0; k < Numlines; k++) {
    if (x <= vocab[k].cum_freq)
      break;
  }
  return k;
}

int str_comp(char *guess, char **options, int len) {  // check whether or not two strings are similar.
  for (int i = 0; i < len; i++) {
    if (strcmp(guess, options[i]) == 0)
      return 0;
  }
  return 1;
}

void game(char *file_occur, int Numlines, word *vocab, char c) {  // game
  int n;
  printf("Remember: Type 'ESC' to exit the game whenever you want. Let's play!\n\n");
  do {
    do {
      n = cond_rand_ind(Numlines, vocab);
    } while (vocab[n].type != c && c != '-');
    char guess[MAX_LEN];
    printf("Foreign word: %s (%s)\nGuess spanish word: ", vocab[n].foreign_word, part_of_speech(vocab[n].type));
    scanf("%[^\n]%*c", guess);  // scan until character '\n' (not included) and scan a character ('\n') and discarted it (with %*c).
    if (strcmp(guess, "ESC") == 0)
      break;
    if (str_comp(guess, vocab[n].spanish_word, vocab[n].Ntrans) == 0) {
      if (vocab[n].occur != 1)
        vocab[n].occur--;
      printf("Correct!\n\n");
    } else {
      vocab[n].occur++;
      printf("Incorrect. The correct answer was: ");  // typing the correct answer
      if (vocab[n].Ntrans == 1)
        printf("'%s'.\n\n", vocab[n].spanish_word[0]);
      else {
        for (int i = 0; i < vocab[n].Ntrans; i++) {
          if (i != vocab[n].Ntrans - 1)
            printf("'%s', ", vocab[n].spanish_word[i]);
          else
            printf("\b\b or %s.\n\n", vocab[n].spanish_word[i]);
        }
      }
    }
    upgrade_content(file_occur, Numlines, vocab);
  } while (1 > 0);
}

char game_mod(word *vocab) {
  printf("Which modality do you want to play?\n");
  printf("1-Only verbs (type 'v')\n2-Only phrasal verbs (type 'P')\n3-Only phrases (type 'p')\n4-Only nouns (type 'n')\n5-Only idioms (type 'i')\n6-Only adjectives (type 'A')\n7-Only adverbs (type 'a')\n8-Any category (type '-')\n");
  char c;
  scanf("%c%*c", &c);  // read one character (stored into &c), the read another one ('\n') and discarted (because of '*').
  if (strcmp(part_of_speech(c), "") == 0 && c != '-') {
    return '1';
  }
  return c;
}

char *part_of_speech(char c) {
  switch (c) {
    case 'v':
      return "verb";
    case 'P':
      return "phrasal verb";
    case 'p':
      return "phrase";
    case 'n':
      return "noun";
    case 'i':
      return "idiom";
    case 'a':
      return "adverb";
    case 'A':
      return "adjective";
    default:
      return "";
  }
}

// Things to do:
// - there's a mystery error while typing some specific combination of keys that produces an ininite bucle.