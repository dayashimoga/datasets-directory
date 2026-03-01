# Technical Requirements & Architecture

## Overview
The Datasets Directory is a statically generated, zero-cost SEO project. It relies on a "boring architecture" principle—meaning it utilizes stable, proven technologies to generate an extremely fast static website without the overhead of runtime servers, databases, or complex frontend frameworks.

## Core Technologies
- **Python 3.11+**: The core scripting language used for data fetching, static site generation, and test automation.
- **Jinja2**: The templating engine used to generate static HTML files from the JSON data.
- **pytest & pytest-cov**: The testing framework used to enforce structural integrity with a >90% code coverage requirement.
- **GitHub Actions**: The CI/CD pipeline responsible for automating tests and deploying to Cloudflare Pages.

## Strict Operational Mandates
1. **Never Assume 200 OK**: Link checkers must intrinsically account for WAF (Web Application Firewall) bots (e.g., HTTP 403, 405, 429) to prevent false-negative deployment crashes.
2. **Synchronized Test Constraints**: Every time a major branch or function is altered, its corresponding Async Pytest mock must be physically rewritten to account for new logical branches.
3. **No Placeholders**: Never upload `database.json` schemas featuring "Sample Data 1". All data schemas must natively inject verified, real-world data entries exceeding 50+ structures.
4. **Git Discipline**: Virtual Environments `.venv` and logging files `*.txt` must immediately map into `.gitignore`. No temporary build artifacts shall pollute the main branches.
5. **UI Differentiation**: Each project requires wholly original semantic structures matching its specific niche (e.g. Tools shouldn't contain language referencing Datasets).

## Project Structure
- `data/`: Contains `database.json`.
- `src/`: Contains `templates/`, `css/`, `js/`, and `images/`.
- `scripts/`: Python scripts responsible for generating HTML (`build_directory.py`) and SEO maps (`generate_sitemap.py`).
- `tests/`: Automated unit tests covering all script functionality.
- `dist/`: The output directory for the final, minified static site assets.

## Operating Principles
1. **Zero-Cost Infrastructure**: The project natively utilizes Cloudflare Pages for extreme distribution bandwidth.
2. **Immutability**: The output `dist/` directory is entirely disposable and re-generated on every build command.
