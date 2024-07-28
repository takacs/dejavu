from schemas import ALL_TABLE_SCHEMAS
from setup_queries import ALL_SETUP_QUERIES

import os

import appdirs
import sqlite3

DB_NAME = "trashman.db"
APP_NAME = "trashman"


def init_db() -> None:
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


if __name__ == "__main__":
    init_db()
