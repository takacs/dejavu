from init_db import init_db
from schemas import ALL_TABLE_SCHEMAS
from setup_queries import ALL_SETUP_QUERIES

import os
from typing import Optional
import sqlite3

import appdirs


DB_NAME = "trashman.db"
APP_NAME = "trashman"


class ConnectionManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self._init_db()
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            self.connection.close()

    def get_connection(self) -> sqlite3.Connection:
        if self.connection is None:
            self._init_db()
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    def _init_db(self) -> None:
        app_folder_path = appdirs.user_data_dir(APP_NAME)
        if not os.path.isdir(app_folder_path):
            print(f"creating {app_folder_path}")
            os.mkdir(app_folder_path)

        # TODO: use Path
        db_file_path = app_folder_path + f"/{DB_NAME}"
        if os.path.isfile(db_file_path):
            print("db exists")
            return

        print(f"creating db file at {db_file_path}")
        with sqlite3.connect(db_file_path) as conn:
            for schema in ALL_TABLE_SCHEMAS:
                conn.execute(schema)
            for query in ALL_SETUP_QUERIES:
                print(query)
                conn.execute(query)
