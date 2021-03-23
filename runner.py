import json
import logging

from counter import Counter
from storage_factory import StorageFactory


def read_config():
    with open("conf.json", 'r') as conf_file:
        return Config(**json.load(conf_file))


class Config:
    def __init__(self, log_level: str = "ERROR", ignore_list=None, storage=None, filenames=None):
        if ignore_list is None:
            ignore_list = []
        if storage is None:
            storage = ["console"]
        if filenames is None:
            storage = []

        self.log_level = log_level
        self.ignore_list = ignore_list
        self.storage = storage
        self.filenames = filenames


if __name__ == "__main__":
    config = read_config()
    logging.basicConfig(level=config.log_level)
    storage_factory = StorageFactory()

    for filename in config.filenames:
        c: Counter = Counter(filename, config.ignore_list)

        for storage_type in config.storage:
            c.add_exporter(storage_factory.produce(storage_type))

        c.get_top_k(100)
