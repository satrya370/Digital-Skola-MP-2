# Course Submission Notes

Project ini berdiri sendiri dan tidak memakai kode frontend/backend blog utama.

## Run

```powershell
cd course-articles-api
python db.py
python app.py
```

Base URL: `http://127.0.0.1:5050`

## Endpoints

```text
GET /articles
GET /articles?source=bbc
GET /articles?title=philosophy
GET /articles?limit=3
GET /articles?source=nytimes&title=attention&limit=5
GET /articles/total
GET /articles/total?ignored=value
```

`source`, `title`, dan `limit` bersifat opsional. `limit` menerima angka 1 sampai 100.

## Expected Total Response

```json
{
  "jumlah_artikel": 12,
  "artikel_bbc": 4,
  "artikel_guardian": 4,
  "artikel_nytimes": 4
}
```

## Screenshot Postman / Browser

Tujuh screenshot endpoint disiapkan melalui Playwright MCP:

1. `screenshots/01-articles-all.png`
2. `screenshots/02-articles-source.png`
3. `screenshots/03-articles-title.png`
4. `screenshots/04-articles-limit.png`
5. `screenshots/05-articles-combined-filter.png`
6. `screenshots/06-articles-total.png`
7. `screenshots/07-articles-invalid-limit.png`

Screenshot ketujuh mendokumentasikan validasi error `limit` sebagai bukti edge case.
