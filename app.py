from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from db import connect, seed_db


HOST = "127.0.0.1"
PORT = 5050


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def article_dict(row) -> dict[str, object]:
    return {
        "id": row["id"],
        "source": row["source"],
        "title": row["title"],
        "content": row["content"],
        "created_at": row["created_at"],
    }


def query_articles(params: dict[str, list[str]]) -> list[dict[str, object]]:
    source = params.get("source", [""])[0].strip()
    title = params.get("title", [""])[0].strip()
    raw_limit = params.get("limit", ["20"])[0].strip()
    try:
        limit = int(raw_limit)
    except ValueError as error:
        raise ValueError("limit must be an integer") from error
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    clauses: list[str] = []
    values: list[object] = []
    if source:
        clauses.append("LOWER(source) = LOWER(?)")
        values.append(source)
    if title:
        clauses.append("LOWER(title) LIKE LOWER(?)")
        values.append(f"%{title}%")
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    values.append(limit)
    with connect() as connection:
        rows = connection.execute(
            f"SELECT id, source, title, content, created_at FROM articles{where} ORDER BY id DESC LIMIT ?",
            values,
        ).fetchall()
    return [article_dict(row) for row in rows]


def article_totals() -> dict[str, int]:
    with connect() as connection:
        total = connection.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        rows = connection.execute(
            "SELECT source, COUNT(*) AS amount FROM articles GROUP BY source ORDER BY source"
        ).fetchall()
    result = {"jumlah_artikel": total}
    for row in rows:
        key = "artikel_" + "_".join(row["source"].lower().split())
        result[key] = row["amount"]
    return result


class ArticleHandler(BaseHTTPRequestHandler):
    def send_json(self, status: int, payload: object) -> None:
        body = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/articles", "/api/articles"):
            try:
                payload = query_articles(parse_qs(parsed.query))
                self.send_json(200, payload)
            except ValueError as error:
                self.send_json(400, {"error": str(error)})
            return
        if parsed.path in ("/articles/total", "/api/articles/total"):
            self.send_json(200, article_totals())
            return
        self.send_json(404, {"error": "Endpoint not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    seeded = seed_db()
    print(f"Articles API running at http://{HOST}:{PORT}")
    print(f"Articles available: {seeded}")
    ThreadingHTTPServer((HOST, PORT), ArticleHandler).serve_forever()
