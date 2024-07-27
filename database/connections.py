import sqlite3
from typing import Optional


class ConnectionManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            self.connection.close()

    def get_connection(self) -> sqlite3.Connection:
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
