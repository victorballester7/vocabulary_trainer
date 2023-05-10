from vars import dict


class word:
    def __init__(self, type: str,
                 foreign_word: list[str], spa_word: list[str], occur: int):
        self.type = type  # type of word (verb, ph-v, noun, adj, adv, prep...)
        # list of strings including the foreign words and parentheses (if any)
        self.foreign_word = foreign_word
        # list of strings including the spanish words and parentheses (if any)
        self.spa_word = spa_word
        self.occur = occur  # weight of the word

    def setFreq(self, cum_freq: float):
        self.cum_freq = cum_freq  # cumulative frequency of the word

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
        self.use_spa_word = S  # list of strings including the spanish words without parentheses

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
        # list of strings including the foreign words without parentheses
        self.use_foreign_word = S

    def wType(self):
        return dict.get(self.type)
