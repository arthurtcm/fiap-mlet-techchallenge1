## TechChallenge1 - Book API

This small Flask application exposes a few read-only endpoints to list and search books and to list available categories. The project uses Flasgger to provide Swagger UI documentation.

Project structure (relevant files):

- `app/src/main.py` - Flask app and route definitions (documented below)
- `app/requirements.txt` - Python dependencies (Flask, pandas, flasgger)
- `app/bases/` - CSV data sources used by the services

## Prerequisites

- Python 3.8+ (or compatible)
- pip

Install dependencies:

```powershell
cd app
pip install -r requirements.txt
```

Run the app (from the repo root):

```powershell
cd app
python src/main.py
```

By default the app runs with `debug=True` on port 5000. Flasgger will expose interactive API docs (usually at `/apidocs`).

## Endpoints (from `app/src/main.py`)

All routes are prefixed with `/api/v1`.

1) List books (paginated)

- Path: `GET /api/v1/books`
- Description: Return a paginated list of books.
- Query parameters:
  - `page` (integer, optional) — page number (default: 1)
  - `total_records` (integer, optional) — items per page (default: 10)
- Responses:
  - `200` — JSON array of book objects.

Example:

```
GET /api/v1/books?page=1&total_records=10

Response 200
[
  { "id": 1, "title": "Example Book", "category": "Fiction", "author": "Author Name" },
  ...
]
```

2) Search books by category or title

- Path: `GET /api/v1/books/search`
- Description: Search books by `category` OR `title`. Only one of `category` or `title` may be provided per request.
- Query parameters:
  - `page` (integer, optional) — page number (default: 1)
  - `total_records` (integer, optional) — items per page (default: 10)
  - `category` (string, optional) — book category (cannot be used together with `title`)
  - `title` (string, optional) — book title (cannot be used together with `category`). If provided, title must be at least 4 characters.
- Validation & responses:
  - If both `category` and `title` are present: `422` with an error message.
  - If neither `category` nor `title` is present: `422` with an error message requesting at least one search parameter.
  - If `title` is provided and its length < 4: `422` with an error message.
  - `200` — JSON array of matched book objects when request is valid.

Examples:

```
GET /api/v1/books/search?category=Science&page=1

Response 200
[
  { "id": 10, "title": "Physics for Everyone", "category": "Science", "author": "A. Scientist" },
  ...
]

GET /api/v1/books/search?title=Magic&page=1

Response 200
[
  { "id": 3, "title": "The Magic World", "category": "Fantasy", "author": "B. Writer" },
  ...
]

GET /api/v1/books/search?category=Fiction&title=Foo

Response 422
{ "error_message": "Não é possível buscar por categoria e titulo ao mesmo tempo" }
```

3) Get book by ID

- Path: `GET /api/v1/books/<id_book>`
- Description: Retrieve a single book by its integer ID.
- Path parameters:
  - `id_book` (integer, required) — ID of the book to fetch
- Responses:
  - `200` — JSON object representing the book (as returned by the service).
  - Note: The docstring mentions `404` for not found, but the current handler returns the service response with HTTP 200; the service implementation determines the exact payload for missing IDs.

Example:

```
GET /api/v1/books/5

Response 200
{ "id": 5, "title": "Some Book", "category": "History", "author": "C. Historian" }
```

4) List categories

- Path: `GET /api/v1/categories`
- Description: Return a list of available book categories.
- Responses:
  - `200` — JSON array of category objects (or strings depending on service implementation).

Example:

```
GET /api/v1/categories

Response 200
[ { "id": 1, "name": "Fiction" }, { "id": 2, "name": "Science" }, ... ]
```

## Notes and assumptions

- The README documents the endpoints as defined in `app/src/main.py`. The exact shape of returned objects depends on the service implementations under `app/src/services/` which read CSV data from `app/bases/`.
- Interactive API docs are available via Flasgger (usually `/apidocs`).
- To run the app successfully, run from the `app` folder so `src` is importable (example commands shown above).

If you'd like, I can also:

- Add example curl/PowerShell commands for each endpoint.
- Extract and show exact example responses by reading the CSVs and running the service functions.

---

Generated from the route definitions present in `app/src/main.py` on November 3, 2025.
# fiap-mlet-techchallenge1