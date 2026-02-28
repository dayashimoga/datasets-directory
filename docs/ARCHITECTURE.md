# Technical Architecture

## System Overview

QuickUtils API Directory is a **Programmatic SEO** static site generator. It fetches data from public API sources, generates thousands of static HTML pages, and deploys them to a CDN for fast, free hosting.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    GitHub Actions (CI/CD)                        â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ Weekly Sync   â”‚  â”‚ Daily Social â”‚  â”‚ CI Tests (on push)   â”‚  â”‚
â”‚  â”‚ (data-sync)   â”‚  â”‚ (social-bot) â”‚  â”‚ pytest + build smoke â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚         â”‚ git push (triggers Netlify rebuild)                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      Build Pipeline                              â”‚
â”‚                                                                  â”‚
â”‚  fetch_data.py â”€â”€â–¶ database.json â”€â”€â–¶ build_directory.py         â”‚
â”‚                                          â”‚                       â”‚
â”‚                                          â”œâ”€â”€â–¶ 30 item pages      â”‚
â”‚                                          â”œâ”€â”€â–¶ 14 category pages  â”‚
â”‚                                          â”œâ”€â”€â–¶ index.html         â”‚
â”‚                                          â””â”€â”€â–¶ 404.html           â”‚
â”‚                                                                  â”‚
â”‚  generate_sitemap.py â”€â”€â–¶ sitemap.xml + robots.txt               â”‚
â”‚                                                                  â”‚
â”‚  Static assets (CSS, JS, ads.txt) â”€â”€â–¶ dist/                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚
          â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Netlify CDN   â”‚â”€â”€â”€â”€â–¶â”‚   End Users     â”‚
â”‚   (free tier)   â”‚     â”‚   + Googlebot   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Code Tree

```
h:\boring\
â”‚
â”œâ”€â”€ .github/workflows/
â”‚   â”œâ”€â”€ ci.yml                 # Runs on push: pytest + coverage + smoke build
â”‚   â”œâ”€â”€ data-sync.yml          # Weekly (Sun 3AM UTC): fetch â†’ commit â†’ push
â”‚   â””â”€â”€ social-bot.yml         # Daily (noon UTC): pick random API â†’ post
â”‚
â”œâ”€â”€ data/
â”‚   â””â”€â”€ database.json          # JSON array of API entries (auto-updated)
â”‚
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ ARCHITECTURE.md        # This file
â”‚   â”œâ”€â”€ SETUP_GUIDE.md         # Deployment & configuration guide
â”‚   â””â”€â”€ TESTING.md             # Test suite documentation
â”‚
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ __init__.py            # Makes scripts a Python package
â”‚   â”œâ”€â”€ utils.py               # Shared constants (paths, slugify, DB I/O)
â”‚   â”œâ”€â”€ fetch_data.py          # Fetches from primary & fallback APIs
â”‚   â”œâ”€â”€ build_directory.py     # SSG engine: Jinja2 â†’ minified HTML
â”‚   â”œâ”€â”€ generate_sitemap.py    # Generates XML sitemap + robots.txt
â”‚   â”œâ”€â”€ post_social.py         # Mastodon auto-poster
â”‚   â”œâ”€â”€ run_tests.ps1          # PowerShell test runner (Docker)
â”‚   â””â”€â”€ run_tests.sh           # Bash test runner (Docker)
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ templates/
â”‚   â”‚   â”œâ”€â”€ base.html          # Master layout (head, header, footer)
â”‚   â”‚   â”œâ”€â”€ index.html         # Homepage (hero, categories, featured)
â”‚   â”‚   â”œâ”€â”€ item.html          # Individual API detail page
â”‚   â”‚   â”œâ”€â”€ category.html      # Category listing with filter
â”‚   â”‚   â””â”€â”€ 404.html           # Custom error page
â”‚   â”œâ”€â”€ css/
â”‚   â”‚   â””â”€â”€ styles.css         # Full design system (~1200 lines)
â”‚   â”œâ”€â”€ js/
â”‚   â”‚   â””â”€â”€ main.js            # Theme toggle, mobile nav, smooth scroll
â”‚   â”œâ”€â”€ ads.txt                # AdSense authorized sellers
â”‚   â””â”€â”€ robots.txt             # Bot directives
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ conftest.py            # Shared fixtures (sample data, tmp dirs)
â”‚   â”œâ”€â”€ test_utils.py          # slugify, DB I/O, categories, truncate
â”‚   â”œâ”€â”€ test_fetch_data.py     # normalize, deduplicate, fetch pipeline
â”‚   â”œâ”€â”€ test_build_directory.py# Jinja env, page gen, static copy, full build
â”‚   â”œâ”€â”€ test_generate_sitemap.py # pages, priority, XML, robots, pipeline
â”‚   â”œâ”€â”€ test_post_social.py    # daily seed, format, Mastodon API, main()
â”‚   â””â”€â”€ test_templates.py      # Template rendering, meta tags, JSON-LD
â”‚
â”œâ”€â”€ .dockerignore              # Excludes dist, venv, caches from Docker
â”œâ”€â”€ .gitignore                 # Comprehensive ignore rules
â”œâ”€â”€ Dockerfile                 # Python 3.11-slim base image
â”œâ”€â”€ docker-compose.yml         # test / build / serve services
â”œâ”€â”€ netlify.toml               # Netlify build config + security headers
â”œâ”€â”€ requirements.txt           # Python dependencies
â””â”€â”€ README.md                  # Project overview and quickstart
```

---

## Module Descriptions

### `scripts/utils.py`
**Purpose**: Shared constants and utility functions used by all other scripts.

| Function | Description |
|---|---|
| `slugify(text)` | Converts text to URL-safe slug (`"Hello World!"` â†’ `"hello-world"`) |
| `load_database(path)` | Reads `data/database.json` into a list of dicts |
| `save_database(items, path)` | Writes sorted JSON with 2-space indent |
| `ensure_dir(path)` | Creates directory and parents if missing |
| `get_categories(items)` | Groups items by category, sorted alphabetically |
| `truncate(text, max_length)` | Truncates text with ellipsis for meta descriptions |

### `scripts/fetch_data.py`
**Purpose**: Fetches API data from public sources with primary + fallback strategy.

- **Primary**: `https://api.publicapis.org/entries` (JSON with `entries` key)
- **Fallback**: `https://raw.githubusercontent.com/public-apis/public-apis/master/json/entries.min.json` (flat JSON array)
- Normalizes fields (`API` â†’ `title`, `Description` â†’ `description`, etc.)
- Deduplicates by title (case-insensitive)
- Saves to `data/database.json`

### `scripts/build_directory.py`
**Purpose**: Static Site Generator using Jinja2 templates.

- Loads database â†’ groups by category
- Generates individual item pages with related items + book recommendations
- Generates category listing pages with filter functionality
- Generates homepage with hero, category cards, and featured APIs
- Generates custom 404 page
- Copies static assets (CSS, JS, ads.txt, robots.txt)
- Minifies HTML output via `htmlmin`

### `scripts/generate_sitemap.py`
**Purpose**: Generates `sitemap.xml` and `robots.txt` for search engine crawling.

- Collects all `.html` files from `dist/`
- Assigns priority (`1.0` index, `0.8` categories, `0.6` items)
- Assigns changefreq (`weekly` index/category, `monthly` items)
- Generates valid XML sitemap with `lastmod`, `priority`, `changefreq`
- Creates `robots.txt` with sitemap reference

### `scripts/post_social.py`
**Purpose**: Automated social media posting to Mastodon.

- Uses date-seeded random selection (same API each day)
- Formats post with title, description, URL, hashtags
- Posts via Mastodon API (`/api/v1/statuses`)
- Keeps posts under 500 character limit

---

## Data Flow

```
1. FETCH PHASE (weekly via GitHub Actions)
   â”œâ”€â”€ GET primary API â†’ normalize entries â†’ deduplicate
   â”œâ”€â”€ If primary fails â†’ GET fallback API â†’ normalize â†’ deduplicate
   â””â”€â”€ Save to data/database.json â†’ git commit â†’ git push

2. BUILD PHASE (triggered by push to main)
   â”œâ”€â”€ Load database.json
   â”œâ”€â”€ Group by category
   â”œâ”€â”€ For each item:
   â”‚   â”œâ”€â”€ Find related items (same category, max 6)
   â”‚   â”œâ”€â”€ Get book recommendations for category
   â”‚   â””â”€â”€ Render item.html â†’ minify â†’ save to dist/api/{slug}.html
   â”œâ”€â”€ For each category:
   â”‚   â””â”€â”€ Render category.html â†’ minify â†’ save to dist/category/{slug}.html
   â”œâ”€â”€ Render index.html â†’ minify â†’ save to dist/index.html
   â”œâ”€â”€ Render 404.html â†’ minify â†’ save to dist/404.html
   â”œâ”€â”€ Copy CSS, JS, ads.txt, robots.txt â†’ dist/
   â””â”€â”€ Generate sitemap.xml + robots.txt â†’ dist/

3. DEPLOY PHASE (Netlify auto-deploy)
   â””â”€â”€ Netlify detects push â†’ runs build â†’ deploys dist/ to CDN

4. SOCIAL PHASE (daily via GitHub Actions)
   â””â”€â”€ Pick random API â†’ format post â†’ POST to Mastodon API
```

---

## SEO Architecture

| Feature | Implementation |
|---|---|
| **Title tags** | Unique per page: `{Title} - Free API \| QuickUtils API Directory` |
| **Meta descriptions** | Auto-truncated to 160 chars from API description |
| **Canonical URLs** | Absolute URLs on every page |
| **Open Graph** | `og:title`, `og:description`, `og:url`, `og:type`, `og:site_name` |
| **Twitter Cards** | `summary_large_image` with title + description |
| **JSON-LD** | `WebSite` (index), `SoftwareApplication` (item), `CollectionPage` (category), `BreadcrumbList` (item + category) |
| **Sitemap** | Auto-generated XML with priority + changefreq per page type |
| **robots.txt** | Auto-generated with sitemap reference |
| **Breadcrumbs** | Visual breadcrumbs + JSON-LD structured data |
| **Semantic HTML** | `<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>` |
| **Favicon** | SVG emoji (âš¡) via data URI â€” zero additional requests |
| **CSS Preload** | `<link rel="preload">` for critical stylesheet |
| **Font Preconnect** | Google Fonts with `preconnect` hints |

---

## Monetization Architecture

| Channel | Implementation |
|---|---|
| **Google AdSense** | Auto ad units on item pages (in-content + sidebar) and index (below featured). Conditional loading â€” only loads when real publisher ID is configured. |
| **Amazon Affiliates** | Curated book recommendations per API category in item page sidebar. Uses affiliate tag from env var. FTC disclosure included. |
| **Gumroad** | "Submit a Tool" CTA in header and CTA section. Paid listing submissions. |
| **Google Analytics** | GA4 tracking on all pages. Conditional â€” only loads with real measurement ID. |

