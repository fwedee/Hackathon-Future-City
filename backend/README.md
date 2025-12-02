## Hackathon-Future-City Backend

### How to use it

- First run `uv sync` to sync the dependencies
- Create a `.env` file based on [.env.example](.env.example) and add your Google Gemini API key:
  - Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
  - Add it to `.env` as `UV_GOOGLE_API_KEY=your-api-key-here`
- Then run `uv run uvicorn app.main:app --reload` (the reload flag is just for development)