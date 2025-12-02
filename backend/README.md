## Hackathon-Future-City Backend

### How to use it

- First run `uv sync` to sync the dependencies
- Create a `.env` file based on [.env.example](.env.example) and add your Google Gemini API key:
  - Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
  - Add it to `.env` as `UV_GOOGLE_API_KEY=your-api-key-here`
- Then run `uv run uvicorn app.main:app --reload` (the reload flag is just for development)

## Structure

```
backend/
├── app/                    # Main application package
│   ├── core/              # Core functionality (database connection, config)
│   ├── models/            # SQLAlchemy database models
│   ├── routers/           # FastAPI route handlers (API endpoints)
│   ├── services/          # Business logic services (planner service)
│   ├── planner/           # OR-Tools optimization logic
│   ├── schemas.py         # Pydantic schemas for request/response validation
│   └── main.py            # FastAPI application entry point
├── seed/                  # Database seeding scripts
├── init_db.py             # Database initialization script
├── hackathon.db           # SQLite database file
├── pyproject.toml         # Project dependencies and configuration
└── .env                   # Environment variables (API keys)
```