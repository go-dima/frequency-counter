from export import Console, CSV, SQLite


class StorageFactory:
    def __init__(self):
        self.factory = {
            "console": lambda: Console(),
            "csv": lambda: CSV("output.csv"),
            "sqlite": lambda: SQLite("sqlite.db")
        }

    def produce(self, storage_key: str):
        if storage_key in self.factory.keys():
            return self.factory[storage_key]()
        else:
            raise KeyError(f"{storage_key} not supported")
