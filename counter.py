import json
import logging
import re
import statistics
from typing import List

from stop_words import get_stop_words

from export import IExport


class Counter:
    def __init__(self, filepath: str):
        self.words_dict = {}
        self.exporters: List[IExport] = []
        self.stop_words = [w.strip('\'') for w in get_stop_words('en')]  # package contains words with '
        self.filepath = filepath
        with open("conf.json", 'r') as conf_file:
            self.conf = json.load(conf_file)
        self._parse_file()

    def _parse_file(self) -> None:
        with open(self.filepath, 'r', encoding="utf8") as file:
            words = file.read()
            as_lowercase = [w.lower() for w in words.replace('\n', ' ').strip().split(' ')]
            no_special = [re.sub(r'\W+', '', w) for w in as_lowercase]
            only_alpha = [w for w in no_special if w.isalpha()]
            no_stop_words = [w for w in only_alpha if w not in self.stop_words and len(w) > 0]
            no_ignored = [w for w in no_stop_words if w not in self.conf["ignore_list"]]
            for word in no_ignored:
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