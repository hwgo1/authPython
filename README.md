# Authentication System API

> A learning project implementing a complete authentication system with JWT tokens.

## About This Project

This is a **learning project** where I'm building a production-grade authentication API from scratch. Each feature is implemented step-by-step following industry best practices, with focus on security and clean architecture.

## Tech Stack

- **Framework:** FastAPI (modern, fast, async-capable)
- **Database:** SQLite (development) / PostgreSQL (production-ready)
- **ORM:** Peewee (lightweight, pythonic)
- **Authentication:** JWT + Refresh Tokens
- **Password Hashing:** bcrypt
- **Validation:** Pydantic

## Features Implemented

### ✅ User Registration

- `/api/register` endpoint
- Password strength requirements
- Uniqueness checks (email and username)
- Secure password hashing with bcrypt

### TODO: Login & Tokens (In Progress)

- Login endpoint with credential verification
- JWT access tokens
- Refresh tokens
- Token-based authentication

## Project Structure

```
authPython/
├── models/          # Database models (User, RefreshToken, etc)
├── routes/          # API endpoints grouped by feature
├── schemas/         # Pydantic schemas for validation
├── utils/           # Helper functions (JWT, hashing, etc)
├── main.py          # Application entry point
└── requirements.txt # Project dependencies
```

## API Documentation

Interactive API docs available at `/docs`

## Running Locally

```bash
# Clone and enter directory
cd authPython

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Access API documentation
open http://127.0.0.1:8000/docs
```

---

This is an **educational project** built to demonstrate understanding of authentication systems and backend development.
