from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "articles.db"


SEED_ARTICLES = [
    ("nytimes", "The Future of Cities", "Urban life is changing through smaller, greener neighborhoods."),
    ("nytimes", "Why Attention Matters", "Attention shapes what people notice, remember, and value."),
    ("nytimes", "The New Climate Economy", "Climate policy is increasingly connected to economic planning."),
    ("nytimes", "Learning in Public", "Sharing the process of learning can improve accountability."),
    ("bbc", "The Quiet Power of Libraries", "Libraries remain important spaces for access and community."),
    ("bbc", "How Rivers Shape History", "Rivers connect trade, migration, and the growth of cities."),
    ("bbc", "A Guide to Better Sleep", "Small changes to routine can improve the quality of rest."),
    ("bbc", "The Science of Memory", "Memory is rebuilt each time a person recalls an experience."),
    ("guardian", "Philosophy in Daily Life", "Philosophy becomes practical when it changes attention and action."),
    ("guardian", "The Value of Slow Thinking", "Taking time to reason can reveal assumptions hidden in quick decisions."),
    ("guardian", "Art and Public Space", "Public art can change how people share and interpret a place."),
    ("guardian", "What Makes a Good Question", "Good questions create room for evidence, doubt, and discovery."),
]


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL CHECK (length(trim(source)) > 0),
                title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                content TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
            CREATE INDEX IF NOT EXISTS idx_articles_title ON articles(title);
            """
        )


def seed_db() -> int:
    init_db()
    with connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        if count:
            return count
        connection.executemany(
            "INSERT INTO articles (source, title, content) VALUES (?, ?, ?)",
            SEED_ARTICLES,
        )
        return len(SEED_ARTICLES)


if __name__ == "__main__":
    print(f"Database ready: {DB_PATH}")
    print(f"Articles available: {seed_db()}")
