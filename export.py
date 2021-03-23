import sqlite3
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


class SQLite(IExport):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        sql_create_words_table = """ CREATE TABLE IF NOT EXISTS words (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        count integer
                                    ); """
        self.conn.execute(sql_create_words_table)
        sql = 'DELETE FROM words'
        cur = self.conn.cursor()
        cur.execute(sql)

    def __del__(self):
        self.conn.close()

    def export(self, to_export: List):
        for item in to_export:
            sql = ''' INSERT INTO words(name,count) VALUES(?,?) '''
            cur = self.conn.cursor()
            cur.execute(sql, item)
            self.conn.commit()


class Console(IExport):
    def export(self, to_export: List):
        pprint(to_export)
