# The Repository
import atexit
import sqlite3
import sys

from dao import _Hats, _Suppliers, _Orders


class _Repository:
    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats (
            id         INTEGER      PRIMARY KEY,
            topping    STRING       NOT NULL,
            supplier   INTEGER,
            quantity   INTEGER      NOT NULL,
            
            FOREIGN KEY(supplier) REFERENCES suppliers(id)
        );

        CREATE TABLE suppliers (
            id       INTEGER   PRIMARY KEY,
            name     STRING    NOT NULL
        );

        CREATE TABLE orders (
            id        INTEGER    PRIMARY KEY,
            location  STRING     NOT NULL,
            hat       INTEGER,     

            FOREIGN KEY(hat) REFERENCES hats(id)

        );
    """)


repo = _Repository(sys.argv[4])
atexit.register(repo.close)
