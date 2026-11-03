# FastAPI Product API

A REST API for a simple product catalogue, built with **FastAPI**, **Pydantic**,
**SQLAlchemy 2.x** and **PostgreSQL**. It supports full CRUD (create, read, update, delete)
on products. Work in progress.

## Endpoints

| Method | Path | What it does |
|---|---|---|
| `GET` | `/` | Welcome message |
| `GET` | `/products` | List all products |
| `GET` | `/products/{id}` | Get one product (404 if it doesn't exist) |
| `POST` | `/products` | Add a product |
| `PUT` | `/products/{id}` | Update a product's fields (404 if it doesn't exist) |
| `DELETE` | `/products/{id}` | Delete a product (404 if it doesn't exist) |

A product looks like this:

```json
{ "id": 1, "name": "Air Fryer", "description": "Home Appliances", "price": 149.0, "quantity": 12 }
```

Request bodies are validated by Pydantic, so a missing field or a wrong type returns a
`422` error with details.

## How to run

Developed and tested with Python 3.15 and PostgreSQL 18.

1. Create an empty PostgreSQL database (for example `products`), using pgAdmin or `createdb products`.
2. Clone the repository and install the dependencies in a virtual environment:

   ```bash
   git clone https://github.com/rroyanirbinna-web/fastapi-product-api.git
   cd fastapi-product-api
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # macOS / Linux
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and put your database details in `DATABASE_URL`.
4. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

5. Open <http://127.0.0.1:8000/docs> to try every endpoint in the interactive Swagger UI.
   The `product` table is created automatically on startup.

## Project structure

| File | Contents |
|---|---|
| `main.py` | The FastAPI app, CORS setup, the `get_db` dependency and the six endpoints |
| `models.py` | Pydantic model that validates request bodies |
| `database_models.py` | SQLAlchemy ORM model for the `product` table |
| `database.py` | Engine and session factory, configured from `DATABASE_URL` |

## Design decisions

1. **API models and database models are separate.** `models.py` (Pydantic) defines what clients
   send and is validated at the boundary; `database_models.py` (SQLAlchemy, using the typed
   `Mapped` / `mapped_column` style) defines the table. Keeping them apart means the API shape and
   the table schema can change independently.
2. **One database session per request.** The `get_db` dependency opens a session, `yield`s it to
   the endpoint, and closes it in a `finally` block, so the connection always goes back to the pool,
   even when the endpoint raises an error.
3. **Configuration comes from the environment.** The database URL is read from `DATABASE_URL`
   (loaded from a local `.env` file with `python-dotenv`), so no credentials are stored in the code.
   `.env` is git-ignored and `.env.example` documents the format. CORS allows a browser front end
   on `http://localhost:3000`.

## Known limitations and next steps

- Clients choose the product `id` in the `POST` body, and an `id` that already exists causes a
  500 error. Next step: let the database generate IDs.
- `POST` returns the request body rather than the saved row, and `PUT` / `DELETE` return plain
  strings. Next step: `response_model` for typed, filtered responses.
- `PUT` updates every field; partial updates with `PATCH` aren't supported yet.
- Tables are created with `create_all` at startup; there are no migrations or automated tests yet.

## Acknowledgements

Built while following Telusko's FastAPI course. During development the API was tested against
an open-source React front end from that course ([front-end repository](ADD-LINK-HERE)),
which is not included in this repository.
