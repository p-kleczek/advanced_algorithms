class RollingHash:
    def __init__(self, string, size):
        self.str = string
        self.hash = sum(map(ord, string[:size]))
        self.init = 0
        self.end = size

    def update(self):
        if self.end <= len(self.str) - 1:
            self.hash += ord(self.str[self.end]) - ord(self.str[self.init])
            self.init += 1
            self.end += 1

    def text(self):
        return self.str[self.init:self.end]


def rabin_karp(substring, string):
    if not substring or not string or len(substring) > len(string):
        return None

    hs = RollingHash(string, len(substring))
    hsub = RollingHash(substring, len(substring))
    hsub.update()

    for i in range(len(string) - len(substring) + 1):
        if hs.hash == hsub.hash and hs.text() == substring:
            return i
        hs.update()

    return None


def knuth_morris_pratt(text, pattern):
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos - shift]:
            shift += shifts[pos - shift]
        shifts[pos + 1] = shift

    start_pos = match_len = 0
    for c in text:
        while match_len == len(pattern) or \
                match_len >= 0 and pattern[match_len] != c:
            start_pos += shifts[match_len]
            match_len -= shifts[match_len]
        match_len += 1
        if match_len == len(pattern):
            yield start_pos
