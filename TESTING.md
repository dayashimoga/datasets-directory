# Testing Data & Coverage Policies

This project implements a non-negotiable >90% code coverage threshold enforced directly through Continuous Integration loops (`pytest-cov`). This ensures that changes to parsing schemas, HTML templates, or data models will never fail silently in production.

## Running Tests Locally
To locally ensure everything is passing, simply utilize our wrapper scripts. You do not need anything installed except Docker.

**Windows:**
```powershell
.\test.ps1
```

**Linux/Mac:**
```bash
./test.sh
```

## Adding New Tests
If you modify `scripts/fetch_data.py`, `scripts/build_directory.py`, `scripts/utils.py`, or any jinja templates in `src/templates`, you must write corresponding assertions in `tests/test_*.py`.

All mock data is managed in `tests/conftest.py`. Rather than performing live HTTP calls for GitHub API queries, data generation acts upon this single source of truth containing mocked standard entries representing the schema elements (such as `name`, `alternative_to`, `github_repo`, etc.).

If a test fails locally, the bash test wrapper will automatically spit out the failing lines to Standard Error, while ensuring the test container destroys itself properly to avoid caching discrepancies (`--rm test`).

### Automated CI
GitHub Actions (`.github/workflows/tests.yml`) spins up headless ubuntu machines and performs the same verification automatically on every pushed commit or pull request. Commits that fail the 90% threshold will block a merge.

