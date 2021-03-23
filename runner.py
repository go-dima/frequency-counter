import re
import logging
import statistics
from typing import List

from export import IExport, CSV, Console


class Counter:
    def __init__(self, filepath: str):
        self.words_dict = {}
        self.exporters: List[IExport] = []
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

    def _top_k(self, k: int) -> List:
        top_k: List = sorted(self.words_dict.items(), key=lambda x: x[1], reverse=True)[:k]
        logging.info(f"Mean:{statistics.mean(map(lambda t: t[1], top_k))}")
        logging.info(f"Median:{statistics.median(map(lambda t: t[1], top_k))}")
        return top_k

    def add_exporter(self, exporter: IExport) -> None:
        self.exporters.append(exporter)

    def get_top_k(self, k: int) -> None:
        top_k = self._top_k(k)
        for exporter in self.exporters:
            exporter.export(top_k)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    c: Counter = Counter("alice.txt")

    e1 = Console()
    c.add_exporter(e1)

    e2 = CSV("output.csv")
    c.add_exporter(e2)

    c.get_top_k(5)


# Assumptions:
# Please do not reinvent the wheel means use existing libs

# TODOs:
# - Remove numbers
# - Accept exporters in ctor?
