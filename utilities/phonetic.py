class Phonetic:

    ALPHABET = {'a': 'alpha', 'b': 'bravo', 'c': 'charlie', 'd' : 'delta',
                'e': 'echo', 'f': 'foxtrot', 'g': 'golf', 'h': 'hotel',
                'i': 'india', 'j': 'juliet', 'k': 'kilo', 'l': 'lima',
                'm': 'mike', 'n': 'november', 'o': 'oscar', 'p': 'papa',
                'q': 'quebec', 'r': 'romeo', 's': 'sierra', 't': 'tango',
                'u': 'uniform', 'v': 'victor', 'w' : 'whiskey', 'x': 'x-ray',
                'y': 'yankee', 'z': 'zulu', '1': 'one', '2': 'two',
                '3': 'three', '4': 'four', '5': 'five', '6': 'six',
                '7': 'seven', '8': 'eight', '9': 'nine', '0': 'zero'}

    def from_phonetic(self, *args):
        args = list(*args)
        letters = []
        for arg in args:
            word = str(arg).lower()
            for key, value in self.ALPHABET.items():
                if value == word:
                    letters.append(key)
        return letters

    def from_phonetic_or_value(self, *args):
        args = list(*args)
        letters = []
        for arg in args:
            word = str(arg).lower()
            match = None
            for key, value in self.ALPHABET.items():
                if value == word:
                    match = key
            letters.append(match or word)
        return letters

    def to_phonetic(self, *args):
        args = list(*args)
        words = []
        for arg in args:
            letter = str(arg).lower()
            if letter in self.ALPHABET:
                words.append(self.ALPHABET[letter])
        return words
