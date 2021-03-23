import re
from pprint import pprint
from typing import List


class Counter:
    def __init__(self, filepath: str):
        self.words_dict = {}
        self.filepath = filepath
        self._parse_file()

    def _parse_file(self) -> None:
        with open(self.filepath, 'r', encoding="utf8") as file:
            words = file.read()
            lowercase = [w.lower() for w in words.replace('\n', ' ').strip().split(' ')]
            only_alpha = [re.sub(r'\W+', '', w) for w in lowercase]
            for word in [w for w in only_alpha if len(w) > 0]:
                if word not in self.words_dict.keys():
                    self.words_dict[word] = 0
                self.words_dict[word] += 1

    def get_top_k(self, k: int) -> List:
        return sorted(self.words_dict.items(), key=lambda x: x[1], reverse=True)[:k]


if __name__ == "__main__":
    c: Counter = Counter("alice.txt")
    pprint(c.get_top_k(5))

# Assumptions:
# Please do not reinvent the wheel means use existing libs

# TODOs:
# - Remove numbers
