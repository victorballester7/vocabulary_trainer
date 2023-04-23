from vars import dict

class word:
  def __init__(self, type: str,
               foreign_word: list[str], spa_word: list[str], occur: int):
    self.type = type
    self.foreign_word = foreign_word
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
    for w in self.foreign_word:
      while w.count("(") > 0:
        if w.index("(") == 0:
          return 1
        try:
          w = w[: w.index("(") - 1] + w[w.index(")") + 1:]
        except ValueError:
          return 1
      S.append(w)
    self.use_foreign_word = S

  def wType(self):
    return dict.get(self.type)
