# Authentication App

A modern, async authentication API built with FastAPI, SQLAlchemy, PostgreSQL, and JWT.  
Includes email verification, secure password hashing, and a modular, production-ready structure.

---

## Features

- **FastAPI** for high-performance async APIs
- **PostgreSQL** with **SQLAlchemy** (async) ORM
- **Alembic** for database migrations
- **JWT** authentication with `python-jose`
- **Password hashing** with `passlib[argon2]`
- **Email verification** via [Resend](https://resend.com/)
- **Environment-based configuration** with `.env` and `pydantic-settings`
- **Role-based access** and OTP support
- **Unique IDs** with `cuid`
- **Redis** support (for caching/sessions)
- **Async HTTP client** with `httpx`
- **Linting** with `ruff`
- **Type checking** with Pylance

---

## Project Structure

```
authentication_app/
├── app/
│   ├── api/           # API routers (v1/auth, etc.)
│   ├── core/          # Settings/config
│   ├── db/            # Database config and models
│   ├── models/        # SQLAlchemy models
│   ├── services/      # Business logic (email, login, etc.)
│   ├── utils/         # Utility functions (CUID, JWT, etc.)
│   └── main.py        # FastAPI app entrypoint
├── tests/             # Pytest-based tests
├── .env               # Environment variables (not tracked)
├── .gitignore         # Ignores secrets, venv, cache, etc.
├── pyproject.toml     # Project metadata and dependencies
├── uv.lock            # Dependency lock file
├── README.md          # Project documentation
```

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/authentication_app.git
cd authentication_app
```

### 2. Set Up Python

- Python **3.13** (see `.python-version`)
- Recommended: Use [pyenv](https://github.com/pyenv/pyenv) or a virtual environment

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
RESEND_API_KEY=your_resend_api_key
RESEND_FROM_EMAIL=your_verified_sender@example.com
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Never commit your `.env` file!**

### 4. Run Database Migrations

```sh
alembic upgrade head
```

### 5. Start the App

```sh
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

---

## Testing

- Tests live in the `tests/` directory.
- Example test command:

```sh
pytest
```

---

## Example API Usage

### Register a User

```sh
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

### Verify a User

```sh
curl -X POST "http://localhost:8000/verify" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "otp": "123456"}'
```

---

## Development

- **Lint:** `ruff .`
- **Type check:** Pylance in VS Code
- **Format:** `ruff format .`

---

## Security

- Passwords are hashed with Argon2 before storage.
- JWTs are signed with a secret key.
- All secrets are loaded from environment variables.

---

## License

MIT License

---

## Author

Fatima

---

## Notes

- This project is under active development.
- Contributions and issues are welcome!
