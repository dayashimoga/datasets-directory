# Testing Documentation

## Overview

The project uses **pytest** with **pytest-cov** for testing and coverage enforcement. The test suite is designed to run inside Docker (zero local installs) with a 90% minimum coverage gate.

---

## Quick Commands

```bash
# Run tests via Docker (recommended)
docker compose run --rm test

# Run tests via Python venv
python -m pytest tests/ -v --cov=scripts --cov-report=term-missing --cov-fail-under=90

# Run a single test file
python -m pytest tests/test_utils.py -v

# Run a single test class
python -m pytest tests/test_build_directory.py::TestBuildSite -v

# Generate HTML coverage report
python -m pytest tests/ --cov=scripts --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Coverage Report

| Module | Stmts | Miss | Coverage | Missing Lines |
|---|---|---|---|---|
| `scripts/__init__.py` | 0 | 0 | **100%** | â€” |
| `scripts/utils.py` | 51 | 1 | **98%** | 60 |
| `scripts/post_social.py` | 62 | 1 | **98%** | 151 |
| `scripts/build_directory.py` | 90 | 6 | **93%** | 41-43, 86, 259, 263 |
| `scripts/generate_sitemap.py` | 82 | 7 | **91%** | 25, 86, 136, 154, 156, 182, 186 |
| `scripts/fetch_data.py` | 82 | 9 | **89%** | 60, 154-155, 167-174, 178 |
| **TOTAL** | **367** | **24** | **93%** | |

**128 tests** â€” **0 failures** â€” **93.46% coverage**

> The CI pipeline enforces `--cov-fail-under=90`. Any PR dropping coverage below 90% will fail.

---

## Test Files

### `tests/conftest.py` â€” Shared Fixtures

| Fixture | Scope | Description |
|---|---|---|
| `sample_items` | function | Returns 3 sample API entries for testing |
| `sample_db` | function | Writes sample items to a temp `database.json` |
| `minimal_templates` | function | Creates minimal Jinja2 templates in a temp directory |

### `tests/test_utils.py` â€” Utility Functions (22 tests)

| Test Class | Tests | What It Covers |
|---|---|---|
| `TestSlugify` | 10 | Basic text, special chars, unicode, empty, numbers, idempotency |
| `TestLoadDatabase` | 4 | Valid JSON, missing file, invalid JSON, non-array JSON |
| `TestSaveDatabase` | 3 | Save + reload, deterministic sorting, auto-create parent dirs |
| `TestEnsureDir` | 2 | New directory creation, existing directory is no-op |
| `TestGetCategories` | 5 | Grouping, alphabetical sort, empty list, uncategorized, all items present |
| `TestTruncate` | 5 | Short text, long text, empty string, None input, exact length |

### `tests/test_fetch_data.py` â€” Data Fetching (18 tests)

| Test Class | Tests | What It Covers |
|---|---|---|
| `TestNormalizeEntry` | 8 | Valid entry, empty auth, missing title/desc, alt key names, whitespace, HTTPS, CORS |
| `TestDeduplicate` | 4 | Removes duplicates, sorted output, empty list, single item |
| `TestFetchFromPrimary` | 5 | Successful fetch, API error, invalid JSON, missing key, network error |
| `TestFetchFromAlternative` | 2 | Successful fetch, failure |
| `TestFetchAndSave` | 3 | Primary success, fallback, all sources fail |

All HTTP calls are mocked using the `responses` library â€” no real network requests during tests.

### `tests/test_build_directory.py` â€” Site Generator (17 tests)

| Test Class | Tests | What It Covers |
|---|---|---|
| `TestCreateJinjaEnv` | 2 | Environment creation, global variables |
| `TestBuildItemPages` | 3 | File generation, meta content, related items |
| `TestBuildCategoryPages` | 2 | File generation, items listed |
| `TestBuildIndexPage` | 3 | File generation, stats, categories listed |
| `TestBuild404Page` | 1 | 404 page generation |
| `TestCopyStaticAssets` | 3 | CSS copy, ads.txt copy, missing dirs handled |
| `TestBuildSite` | 3 | Full pipeline, empty database, old dist cleanup |

### `tests/test_generate_sitemap.py` â€” Sitemap Builder (18 tests)

| Test Class | Tests | What It Covers |
|---|---|---|
| `TestCollectPages` | 5 | Collects HTML, excludes 404, sorted, forward slashes, empty dir |
| `TestGetPriority` | 4 | Index (1.0), category (0.8), API (0.6), other (0.4) |
| `TestGetChangefreq` | 3 | Index/category (weekly), API (monthly) |
| `TestBuildSitemapXml` | 6 | Valid XML, all URLs, index=root, lastmod, priority, empty |
| `TestBuildRobotsTxt` | 2 | Contains sitemap URL, allows all bots |
| `TestGenerateSitemap` | 5 | Creates sitemap, robots.txt, no-overwrite robots, empty dist, all pages |

### `tests/test_post_social.py` â€” Social Media Bot (16 tests)

| Test Class | Tests | What It Covers |
|---|---|---|
| `TestGetDailySeed` | 3 | Returns integer, deterministic same day, different days |
| `TestPickRandomItem` | 3 | Picks from list, deterministic, single item |
| `TestFormatPost` | 8 | Contains title/desc/URL/hashtags, within 500 chars, auth info, HTTPS, truncation |
| `TestPostToMastodon` | 5 | Successful post, missing token, API error, custom URL, network error |
| `TestMain` | 3 | CLI with items, empty database, successful post |

### `tests/test_templates.py` â€” Template Rendering (13 tests)

| Test Class | Tests | What It Covers |
|---|---|---|
| `TestBaseTemplate` | 5 | Title rendering, meta description, GA script, AdSense, Open Graph |
| `TestItemTemplate` | 5 | Item data, JSON-LD, breadcrumbs, ad slots, related items |
| `TestCategoryTemplate` | 2 | Category rendering, search filter |
| `TestErrorTemplate` | 1 | 404 page rendering |

---

## CI Pipeline (`.github/workflows/ci.yml`)

```yaml
# Triggers: push to main, pull requests to main
# Steps:
#   1. Checkout code
#   2. Set up Python 3.11
#   3. Install dependencies
#   4. Run pytest with coverage (fail if <90%)
#   5. Smoke test: build the full site
```

The CI pipeline runs on every push and PR. It:
- Fails if any test fails
- Fails if coverage drops below 90%
- Runs a smoke build to verify the site generates correctly

---

## Writing New Tests

### Test File Convention
- File name: `tests/test_{module_name}.py`
- Class name: `Test{FeatureName}`
- Method name: `test_{specific_behavior}`

### Common Patterns

**Mocking HTTP requests:**
```python
import responses

@responses.activate
def test_api_call(self):
    responses.add(responses.GET, "https://api.example.com/data",
                  json={"key": "value"}, status=200)
    result = my_function()
    assert result == expected
```

**Patching environment variables:**
```python
from unittest.mock import patch

def test_with_env(self):
    with patch.dict("os.environ", {"MY_VAR": "value"}):
        result = my_function()
    assert result == expected
```

**Using temp directories:**
```python
def test_file_creation(self, tmp_path):
    output = tmp_path / "output.html"
    my_function(output_path=output)
    assert output.exists()
    assert "expected content" in output.read_text()
```

### Running with Verbose Output

```bash
# Show each test name and pass/fail
python -m pytest tests/ -v

# Show print statements during tests
python -m pytest tests/ -v -s

# Stop on first failure
python -m pytest tests/ -x

# Show local variables in tracebacks
python -m pytest tests/ --tb=long
```

