from pprint import pprint
from abc import abstractmethod, ABC
from typing import List


class IExport(ABC):
    @abstractmethod
    def export(self, to_export: List):
        raise NotImplementedError


class CSV(IExport):
    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def export(self, to_export):
        with open(self.filepath, 'w') as csv_file:
            for item in to_export:
                print(f"{item[0]}, {item[1]}", file=csv_file)


class SQL(IExport):
    def __init__(self):
        pass

    def export(self, to_export: List):
        pass


class Console(IExport):
    def export(self, to_export: List):
        pprint(to_export)
