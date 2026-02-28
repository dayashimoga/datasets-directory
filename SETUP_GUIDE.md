# Setup Guide

This project is built from the ground up for zero-dependency local verification using Docker. Follow these steps to set up the Public Datasets Directory locally.

## Prerequisites
- **Git**
- **Docker & Docker Compose**: The *only* other piece of required software.

## 1. Automated Setup & Serving (Recommended)
You can build, test, and serve the directory site locally using the provided automation scripts:

**On Windows (PowerShell):**
```powershell
.\test.ps1
```
**On macOS/Linux:**
```bash
./test.sh
```

### What does the test script do?
1. Builds a fresh Docker container to handle the Python 3.11 environment (`Dockerfile`).
2. Installs `requirements.txt`.
3. Re-downloads the live database (`scripts/fetch_data.py`).
4. Rebuilds the entire site structure and static assets (`scripts/build_directory.py`).
5. Generates the `sitemap.xml` and `robots.txt` (`scripts/generate_sitemap.py`).
6. Executes the entire `pytest` test suite, enforcing a >90% code coverage rule.
7. Boots a local HTTP server using Docker so you can test the site physically on `http://localhost:8000`.

## 2. Docker Execution (Manual)
If you want to manually run scripts without running tests or spawning the web server:

```bash
docker compose run --rm test python scripts/fetch_data.py
docker compose run --rm test python scripts/build_directory.py
```

## 3. Directory Layout
You only need to interact with the following areas during active development:
- **`data/database.json`**: Use carefully encoded JSON elements corresponding to `name`, `alternative_to`, `github_repo`, etc. This file is overwritten automatically by `fetch_data.py` relying on a central database, or defaults to the included seed database on fetch failure.
- **`src/templates/`**: These files use the Jinja2 context to map directly to their endpoints in `/dist`. When modifying `item.html`, the variable `{{ item.alternative_to }}` dictates the payload data.
- **`tests/`**: Contains pytest test files and mock fixtures enforcing coverage. When editing schemas, ensure you change variables in `tests/conftest.py` first.

