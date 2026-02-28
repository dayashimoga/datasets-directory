"""
Shared utilities for the Programmatic SEO Directory.
"""
import json
import os
import re
import unicodedata
from pathlib import Path

# Project root is one level up from scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DIST_DIR = PROJECT_ROOT / "dist"
SRC_DIR = PROJECT_ROOT / "src"
TEMPLATES_DIR = SRC_DIR / "templates"

SITE_URL = os.environ.get("SITE_URL", "https://directory.quickutils.top")
SITE_NAME = "QuickUtils Public Datasets"
SITE_DESCRIPTION = "The Ultimate Directory of Free, Public Datasets — searchable, categorized, and always up-to-date."


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug.

    Examples:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("  Spaces & Symbols!! ")
        'spaces-symbols'
        >>> slugify("Ünïcödé Têxt")
        'unicode-text'
    """
    # Normalize unicode to ASCII
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # Lowercase
    text = text.lower()
    # Replace non-alphanumeric with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Strip leading/trailing hyphens
    text = text.strip("-")
    # Collapse multiple hyphens
    text = re.sub(r"-{2,}", "-", text)
    return text


def load_database(path: Path = None) -> list:
    """Load the database JSON file and return a list of items.

    Args:
        path: Optional path to the database file. Defaults to data/database.json.

    Returns:
        List of item dictionaries.

    Raises:
        FileNotFoundError: If the database file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    if path is None:
        path = DATA_DIR / "database.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("database.json must contain a JSON array")

    return data


def save_database(items: list, path: Path = None) -> None:
    """Save items to the database JSON file with deterministic sorting.

    Args:
        items: List of item dictionaries.
        path: Optional path. Defaults to data/database.json.
    """
    if path is None:
        path = DATA_DIR / "database.json"

    ensure_dir(path.parent)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def ensure_dir(path: Path) -> None:
    """Create a directory and its parents if they don't exist."""
    path.mkdir(parents=True, exist_ok=True)


def get_categories(items: list) -> dict:
    """Group items by category.

    Args:
        items: List of item dicts, each with a 'category' key.

    Returns:
        Dict mapping category name -> list of items.
    """
    categories = {}
    for item in items:
        cat = item.get("category", "Uncategorized")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    # Sort categories alphabetically
    return dict(sorted(categories.items()))


def truncate(text: str, max_length: int = 160) -> str:
    """Truncate text to max_length, adding ellipsis if needed."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rsplit(" ", 1)[0] + "..."
