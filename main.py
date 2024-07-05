# imports
import sqlite3
from typing import List, Optional, Any
cursor = None

class DB_Cursor:
    __cursor = None

    @staticmethod
    def get_cursor():
        if DB_Cursor.__cursor:
            return DB_Cursor.__cursor
        else:
            conn = sqlite3.connect('tracker.db')
            DB_Cursor.__cursor = conn.cursor()
            return DB_Cursor.__cursor




def create_tables():
    create_table_statements: List[str] = ['''
                                          CREATE TABLE tags (
                                          tag_id INTEGER PRIMARY KEY, 
                                          tag_name TEXT);
                                          ''', 
                                          '''
                                        CREATE TABLE IF NOT EXISTS sessions (
                                        session_id INTEGER PRIMARY KEY,
                                        session_name TEXT,
                                        session_start INTEGER, 
                                        session_end INTEGER
                                        );
                                        ''', 
                                        '''
                                        CREATE TABLE activity (
                                        acitivty_id INTEGER PRIMARY KEY,
                                        application_name TEXT NOT NULL,
                                        is_browser INTEGER NOT NULL CHECK (is_browser = 0 or is_browser = 1),
                                        url TEXT,
                                        title TEXT NOT NULL,
                                        start_time INTEGER NOT NULL,
                                        end_time INTEGER NOT NULL,
                                        tag_id INTEGER,
                                        session_id INTEGER,
                                        FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
                                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                                        );
                                        ''']
    try:
        cursor = DB_Cursor.get_cursor()
        for statement in create_table_statements:
            cursor.execute(statement)
    except Exception as e:
        print(e)
        raise e


def main():
    create_tables()
    print()


if __name__ == "__main__":
    main()