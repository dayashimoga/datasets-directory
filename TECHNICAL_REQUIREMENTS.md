# Technical Requirements & Architecture

## Overview
The public datasets Directory is a statically generated, zero-cost SEO project. It relies on a "boring architecture" principleâ€”meaning it utilizes stable, proven technologies to generate an extremely fast static website without the overhead of runtime servers, databases, or complex frontend frameworks.

## Core Technologies
- **Python 3.11+**: The core scripting language used for data fetching, static site generation, and test automation.
- **Jinja2**: The templating engine used to generate static HTML files from the JSON data.
- **Docker & Docker Compose**: Used to encapsulate the local development and testing environments, ensuring no host machine dependencies are required.
- **pytest & pytest-cov**: The testing framework used to enforce structural integrity with a >90% code coverage requirement.
- **GitHub Actions**: The CI/CD pipeline responsible for automating tests and deploying to Cloudflare Pages.

## Project Structure
- `data/`: Contains `database.json`, the single source of truth for the directory.
- `src/`: Contains `templates/`, `css/`, `js/`, and `images/` which act as the raw assets for the site generator.
- `scripts/`: Python scripts responsible for downloading data (`fetch_data.py`), generating HTML (`build_directory.py`), building SEO maps (`generate_sitemap.py`), and posting to social media (`post_social.py`).
- `tests/`: Automated unit tests covering all script functionality.
- `dist/`: The output directory for the final, minified static site assets.

## Operating Principles
1. **API/Data Driven**: The site is rebuilt nightly by fetching the latest public datasets data, ensuring the content remains fresh without manual intervention.
2. **Zero-Cost Infrastructure**: The project uses Cloudflare Pages for hosting and Mastodon for free social media promotion. Analytics and monetization are integrated purely via static tags.
3. **Immutability**: The output `dist/` directory is entirely disposable and re-generated on every build command.

