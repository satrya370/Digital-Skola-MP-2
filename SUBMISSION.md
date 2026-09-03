# Course Submission Notes

Project ini berdiri sendiri dan tidak memakai kode frontend/backend blog utama.

## Run

```powershell
cd <folder-repository>
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

Contoh URL yang bisa langsung dipakai di Postman:

```text
http://127.0.0.1:5050/articles?source=bbc&title=memory&limit=2
http://127.0.0.1:5050/articles/total
```

## Expected Total Response

```json
{
  "jumlah_artikel": 12,
  "artikel_bbc": 4,
  "artikel_guardian": 4,
  "artikel_nytimes": 4
}
```

## Postman Collection

Import file `postman/articles-api.postman_collection.json` ke Postman. Collection ini berisi tujuh request untuk kebutuhan screenshot.

## Screenshot Postman / Browser

Tujuh screenshot endpoint disiapkan melalui Postman:

1. `screenshot/Screenshot 2026-09-03 152918.png`
2. `screenshot/Screenshot 2026-09-03 153016.png`
3. `screenshot/Screenshot 2026-09-03 153034.png`
4. `screenshot/Screenshot 2026-09-03 153048.png`
5. `screenshot/Screenshot 2026-09-03 153111.png`
6. `screenshot/Screenshot 2026-09-03 153127.png`
7. `screenshot/Screenshot 2026-09-03 153143.png`

Screenshot ketujuh mendokumentasikan validasi error `limit` sebagai bukti edge case.
