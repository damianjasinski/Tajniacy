import sys


class WordReader:
    def __init__(self):
        self.words = tuple()
        self.read = False

    def read_file(self, filename):
        with open(filename, "rt", encoding="utf-8") as file:
            wordsTable = list()
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                if line[0] == "#":
                    continue
                wordsTable.append(line)
            self.words = tuple(wordsTable)
        self.read = True

    def get_words(self):
        if self.read:
            return self.words
        else:
            return None


if __name__ == "__main__":
    fr = WordReader()
    fr.read_file("words.txt")
    for w in fr.get_words():
        print(w)
