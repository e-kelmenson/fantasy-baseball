# Notes App

A small Flask web app for practicing backend development. Users can create an account, log in, and manage personal notes.

## Features

- Sign up, log in, and log out
- Create and delete notes
- Associate notes with the user who created them
- Render pages with Flask and Jinja templates

## Built With

- Python 3.12
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Jinja
- pytest

## Configuration

`main.py` calls `load_dotenv()` before creating the Flask app. The `python-dotenv` package reads `.env` and makes its values available as environment variables. The app then reads `SECRET_KEY` from the environment. In deployment, the environment variable can be provided by the hosting platform instead of a `.env` file.

Locally, the app reads `SECRET_KEY` from `practice/flask_webapp/.env`.

Generate a key with:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Copy the generated value into a local `.env` file:

`SECRET_KEY=your-generated-value`

`.env` is ignored by Git and must not be committed.

The app uses SQLite by default; `DATABASE_URL` can select another database.

## Run Locally

From the `practice/flask_webapp` directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
