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
python app.py
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
GET /api/v1/books?page=1&total_records=3

Response 200
{
    "books": [
        {
            "categoria": "Travel",
            "disponibilidade": "In stock",
            "id": 0,
            "imagem": "../../../../media/cache/27/a5/27a53d0bb95bdd88288eaf66c9230d7e.jpg",
            "link": "../../../its-only-the-himalayas_981/index.html",
            "preco": "Â£45.17",
            "rating": "Two",
            "titulo": "It's Only the Himalayas"
        },
        {
            "categoria": "Travel",
            "disponibilidade": "In stock",
            "id": 1,
            "imagem": "../../../../media/cache/57/77/57770cac1628f4407636635f4b85e88c.jpg",
            "link": "../../../full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html",
            "preco": "Â£49.43",
            "rating": "Four",
            "titulo": "Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond"
        },
        {
            "categoria": "Travel",
            "disponibilidade": "In stock",
            "id": 2,
            "imagem": "../../../../media/cache/9a/7e/9a7e63f12829df4b43b31d110bf3dc2e.jpg",
            "link": "../../../see-america-a-celebration-of-our-national-parks-treasured-sites_732/index.html",
            "preco": "Â£48.87",
            "rating": "Three",
            "titulo": "See America: A Celebration of Our National Parks & Treasured Sites"
        }
    ],
    "info": {
        "pagina_atual": 1,
        "total_registros": 1000,
        "total_registros_retornados": 3
    }
}
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
GET /api/v1/books/search?category=Science&page=1&total_records=2

Response 200
{
    "books": [
        {
            "categoria": "Science",
            "disponibilidade": "In stock",
            "id": 798,
            "imagem": "../../../../media/cache/d4/8d/d48d5122a15347e9fe2b15ad354d69bf.jpg",
            "link": "../../../the-most-perfect-thing-inside-and-outside-a-birds-egg_938/index.html",
            "preco": "Â£42.96",
            "rating": "Four",
            "titulo": "The Most Perfect Thing: Inside (and Outside) a Bird's Egg"
        },
        {
            "categoria": "Science",
            "disponibilidade": "In stock",
            "id": 799,
            "imagem": "../../../../media/cache/26/1c/261c4eaf957ae4aacf2229b482e76dbe.jpg",
            "link": "../../../immunity-how-elie-metchnikoff-changed-the-course-of-modern-medicine_900/index.html",
            "preco": "Â£57.36",
            "rating": "Five",
            "titulo": "Immunity: How Elie Metchnikoff Changed the Course of Modern Medicine"
        }
    ],
    "info": {
        "pagina_atual": 1,
        "total_registros": 14,
        "total_registros_retornados": 2
    }
}

GET /api/v1/books/search?title=Magic&page=1&total_records=2

Response 200
{
    "books": [
        {
            "categoria": "Nonfiction",
            "disponibilidade": "In stock",
            "id": 333,
            "imagem": "../../../../media/cache/95/64/95647d6a526bf54120b9445e124794e1.jpg",
            "link": "../../../the-life-changing-magic-of-tidying-up-the-japanese-art-of-decluttering-and-organizing_936/index.html",
            "preco": "Â£16.77",
            "rating": "Three",
            "titulo": "The Life-Changing Magic of Tidying Up: The Japanese Art of Decluttering and Organizing"
        },
        {
            "categoria": "Nonfiction",
            "disponibilidade": "In stock",
            "id": 348,
            "imagem": "../../../../media/cache/62/ad/62ad9b4077416ddc0c4908062bca0e5e.jpg",
            "link": "../../../big-magic-creative-living-beyond-fear_796/index.html",
            "preco": "Â£30.80",
            "rating": "Three",
            "titulo": "Big Magic: Creative Living Beyond Fear"
        }
    ],
    "info": {
        "pagina_atual": 1,
        "total_registros": 1000,
        "total_registros_retornados": 2
    }
}

GET /api/v1/books/search?category=Fiction&title=Art

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
GET /api/v1/books/1

Response 200
{
    "books": [
        {
            "categoria": "Travel",
            "disponibilidade": "In stock",
            "id": 1,
            "imagem": "../../../../media/cache/57/77/57770cac1628f4407636635f4b85e88c.jpg",
            "link": "../../../full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html",
            "preco": "Â£49.43",
            "rating": "Four",
            "titulo": "Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond"
        }
    ]
}
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
{
    "categories": [
        {
            "link": "catalogue/category/books/travel_2/index.html",
            "nome": "Travel"
        },
        {
            "link": "catalogue/category/books/mystery_3/index.html",
            "nome": "Mystery"
        },
        ...
    ]
}
```
---

# fiap-mlet-techchallenge1