# CLAUDE.md

## Project Overview

**Direct Print** is a Django REST API that enables direct printing to local client printers via HTTP. It accepts file uploads through a REST endpoint and sends them to a Windows printer using the `win32api`/`win32print` libraries. It also provides an endpoint to list and register printers.

**Repository:** `thawat-th/direct_print`

## Tech Stack

- **Language:** Python 3
- **Framework:** Django 3.0.8 + Django REST Framework 3.11.0
- **Database:** SQLite3 (default Django backend)
- **API Documentation:** drf-yasg 1.17.1 (Swagger/OpenAPI + ReDoc)
- **Printing:** pywin32 228 (Windows-only: `win32api`, `win32print`)
- **CORS:** django-cors-headers 3.4.0
- **Image Processing:** Pillow 7.2.0

## Project Structure

```
direct_print/
├── manage.py                      # Django management entry point
├── requirements.txt               # Python dependencies (pinned versions)
├── README.md                      # Setup instructions
├── .gitignore                     # Python/Django/IDE ignores
├── direct_print/                  # Django project configuration
│   ├── __init__.py
│   ├── settings.py                # Settings (DEBUG, DB, installed apps, REST config)
│   ├── urls.py                    # Root URL routing (Swagger, admin, API include)
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
└── api/                           # Main API application
    ├── __init__.py
    ├── models.py                  # Printer and Print models
    ├── views.py                   # PrintFileView, PrinterView
    ├── serializers.py             # PrinterSerializer, PrintFileSerializer
    ├── urls.py                    # API routes (/v1/print, /v1/printers)
    ├── admin.py                   # Admin registration for Print model
    ├── apps.py                    # App config
    ├── forms.py                   # Empty (commented-out code)
    ├── tests.py                   # Empty placeholder
    └── migrations/
        └── __init__.py            # No migrations generated yet
```

## API Endpoints

| Method | Path           | View            | Description                          |
|--------|----------------|-----------------|--------------------------------------|
| POST   | `/v1/print`    | PrintFileView   | Upload a file and print it           |
| GET    | `/v1/printers` | PrinterView     | List all registered printers         |
| POST   | `/v1/printers` | PrinterView     | Register a new printer               |
| GET    | `/docs/`       | Swagger UI      | Interactive API documentation        |
| GET    | `/redoc/`      | ReDoc UI        | Alternative API documentation        |
| GET    | `/docs.json`   | Schema (JSON)   | OpenAPI schema in JSON               |
| GET    | `/docs.yaml`   | Schema (YAML)   | OpenAPI schema in YAML               |
| GET    | `/admin/`      | Django Admin    | Admin interface                      |

## Development Setup

```bash
# Clone
git clone https://github.com/thawat-th/direct_print.git
cd direct_print

# Virtual environment
pip install --upgrade --force virtualenv
virtualenv venv

# Activate (Linux/macOS)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (required before first run)
python manage.py migrate

# Start development server
python manage.py runserver 8000
```

The server runs at `http://localhost:8000`. Swagger docs are at `/docs/`.

## Common Commands

```bash
python manage.py runserver 8000      # Start dev server on port 8000
python manage.py migrate             # Apply database migrations
python manage.py makemigrations      # Generate new migrations after model changes
python manage.py createsuperuser     # Create admin user
python manage.py collectstatic       # Collect static files for deployment
python manage.py shell               # Open Django interactive shell
```

## Key Architecture Details

### Models (`api/models.py`)
- **Printer** - Stores printer names (`printer_name` field, defined as `TextField` reference without parentheses — this is a known bug)
- **Print** - Stores uploaded files (`file` FileField)

### Views (`api/views.py`)
- **PrintFileView** (CreateAPIView) — Accepts multipart file upload, saves to DB, then prints to the Windows default printer via `win32api.ShellExecute`
- **PrinterView** (APIView) — GET lists printers, POST registers a new printer. Note: both methods use `PrintFileSerializer` instead of `PrinterSerializer` — this appears to be a bug

### Serializers (`api/serializers.py`)
- **PrinterSerializer** — ModelSerializer for Printer
- **PrintFileSerializer** — ModelSerializer for Print

### Settings (`direct_print/settings.py`)
- REST Framework is configured with FileUpload, Form, MultiPart, and JSON parsers
- CORS is fully open (`CORS_ORIGIN_ALLOW_ALL = True`)
- CorsMiddleware is placed between SessionMiddleware and CommonMiddleware (correct order)

## Known Issues

1. **`Printer.printer_name`** is defined as `models.TextField` (class reference) instead of `models.TextField()` (instance) — the field will not work correctly
2. **PrinterView** uses `PrintFileSerializer` instead of `PrinterSerializer` in both GET and POST methods
3. **No migrations** have been generated — `api/migrations/` is empty
4. **No tests** exist — `api/tests.py` is a placeholder
5. **Windows-only** — `win32api`/`win32print` imports will fail on Linux/macOS; the printing functionality requires Windows
6. **Security** — `SECRET_KEY` is hardcoded, `DEBUG = True`, `ALLOWED_HOSTS` is empty, CORS allows all origins
7. **No authentication** on any API endpoint

## Conventions and Patterns

- **Django project layout:** Standard two-level structure (`direct_print/` project config + `api/` app)
- **DRF class-based views:** Uses `CreateAPIView` and `APIView` from Django REST Framework
- **URL versioning:** API paths are prefixed with `/v1/`
- **Serializers:** ModelSerializer pattern with `fields = "__all__"`
- **File uploads:** Handled via DRF's `MultiPartParser`
- **No linters/formatters configured** — no `.flake8`, `pyproject.toml`, `black`, or `isort` config
- **No CI/CD** — no GitHub Actions, no test automation
- **No `.env` usage** — secrets and config are hardcoded in `settings.py`

## Guidelines for AI Assistants

- **Platform awareness:** The printing functionality (`win32api`, `win32print`) only works on Windows. Any changes to printing logic must account for this. On non-Windows systems, these imports will fail.
- **Migrations:** If modifying models, always run `python manage.py makemigrations` followed by `python manage.py migrate`. Note that no migrations currently exist.
- **Serializer bug:** `PrinterView` uses the wrong serializer. If fixing the printer endpoints, switch to `PrinterSerializer`.
- **Model bug:** `Printer.printer_name = models.TextField` is missing parentheses. This needs to be `models.TextField()` to function.
- **No test infrastructure:** There are no existing tests. If adding tests, use Django's built-in `TestCase` from `django.test` and DRF's `APITestCase` from `rest_framework.test`.
- **Dependencies:** All versions are pinned in `requirements.txt`. Update the file when adding/changing dependencies.
- **Keep it simple:** This is a small utility project. Avoid over-engineering or adding complex abstractions.
