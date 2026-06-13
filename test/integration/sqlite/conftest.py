from __future__ import annotations

import sqlite3
from collections.abc import Generator

import pytest


@pytest.fixture()
def sqlite_conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        INSERT INTO users (id, name, email) VALUES
            (1, 'Joao', 'joao@email.com'),
            (2, 'Maria', 'maria@email.com'),
            (3, 'Pedro', 'pedro@email.com');

        INSERT INTO transactions (id, user_id, amount, date) VALUES
            (1, 1, 100.0, '2024-01-01'),
            (2, 1, -50.0, '2024-01-15'),
            (3, 2, 200.0, '2024-02-01'),
            (4, 2, -30.0, '2024-02-15'),
            (5, 2, 80.0, '2024-03-01'),
            (6, 3, 500.0, '2024-01-10'),
            (7, 1, 25.0, '2024-02-20');
    """)
    yield conn
    conn.close()
