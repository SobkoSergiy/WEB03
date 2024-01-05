from pathlib import Path
import sqlite3


def create_tables():
    sql = Path('create_tables.sql').read_text()
    print(sql)

    with sqlite3.connect('modul06.db') as con:
        cur = con.cursor()
        cur.executescript(sql)

    print("Tables created")



def main():
    create_tables()

if __name__ == "__main__":
    main()