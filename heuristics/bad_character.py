from heuristics.heuristics import Heuristic


class BadCharacter(Heuristic):

    def preprocess(self, pattern, alphabet=None):
        self.map = {}
        for i in range(len(alphabet)):
            self.map[alphabet[i]] = i
        self.dense_bad_char_tab = []
        nxt = [0] * len(self.map)

        for i in range(0, len(pattern)):
            c = pattern[i]
            self.dense_bad_char_tab.append(nxt[:])
            nxt[self.map[c]] =i + 1

    def get_offset_matched(self, **kwargs):
        return 0

    def get_offset_mismatched(self, **kwargs):
        c = kwargs['cur_letter']
        i = kwargs['mismatch_offset']
        ci = self.map[c]
        return i - (self.dense_bad_char_tab[i][ci] - 1)

    def get_name(self):
        return "Bad character"
