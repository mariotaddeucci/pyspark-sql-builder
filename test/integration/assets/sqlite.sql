CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    region_id INTEGER NOT NULL
);

INSERT INTO users (id, name, email, region_id) VALUES
    (1, 'Joao', 'joao@email.com', 1),
    (2, 'Maria', 'maria@email.com', 2),
    (3, 'Pedro', 'pedro@email.com', 1);

CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO regions (region_id, name) VALUES
    (1, 'North'),
    (2, 'South');

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    category_id INTEGER NOT NULL
);

INSERT INTO transactions (id, user_id, amount, date, category_id) VALUES
    (1, 1, 100.0, '2024-01-01', 1),
    (2, 1, -50.0, '2024-01-15', 2),
    (3, 2, 200.0, '2024-02-01', 3),
    (4, 2, -30.0, '2024-02-15', 2),
    (5, 2, 80.0, '2024-03-01', 3),
    (6, 3, 500.0, '2024-01-10', 1),
    (7, 1, 25.0, '2024-02-20', 1);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO categories (id, name) VALUES
    (1, 'food'),
    (2, 'transport'),
    (3, 'entertainment');
