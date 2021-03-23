import logging

from counter import Counter
from export import CSV, Console, SQLite

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    c: Counter = Counter("alice.txt")

    e1 = Console()
    c.add_exporter(e1)

    e2 = CSV("output.csv")
    c.add_exporter(e2)

    e3 = SQLite("sqlite.db")
    c.add_exporter(e3)

    c.get_top_k(5)
