"""Script to validate all external URLs in the database."""
import asyncio
import argparse
import json
import logging
import sys
from collections import defaultdict
from pathlib import Path

import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "database.json"

# Timeout for requests
TIMEOUT = aiohttp.ClientTimeout(total=15)

# Use a standard user agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def check_url(session: aiohttp.ClientSession, url: str) -> tuple[str, bool, str]:
    """Check a single URL, return (url, is_valid, error_msg)."""
    if not url:
        return url, False, "Empty URL"

    try:
        # Try HEAD first, fallback to GET if HEAD isn't fully supported
        async with session.head(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS) as response:
            if response.status < 400:
                return url, True, ""
            if response.status == 405: # Method not allowed fallback
                async with session.get(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS) as get_resp:
                    if get_resp.status < 400:
                        return url, True, ""
                    return url, False, f"GET returned HTTP {get_resp.status}"
            return url, False, f"HEAD returned HTTP {response.status}"
    except asyncio.TimeoutError:
        return url, False, "Connection timed out"
    except aiohttp.ClientError as e:
        return url, False, f"Client error: {str(e)}"
    except Exception as e:
        return url, False, f"Unexpected error: {str(e)}"


async def main_async(fail_fast: bool) -> tuple[int, int, int, dict]:
    """Asynchronous entry point. Returns (total_items, total_links, broken, report_dict)."""
    if not DB_PATH.exists():
        logger.error(f"Database not found at {DB_PATH}")
        sys.exit(1)

    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            items = json.load(f)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse {DB_PATH} as JSON.")
        sys.exit(1)

    # Collect all URLs
    urls_to_check: set[str] = set()
    url_to_titles: dict[str, list[str]] = defaultdict(list)

    for item in items:
        title = item.get("title", "Unknown Item")
        # Check standard URL
        url = item.get("url")
        if url:
            urls_to_check.add(url)
            url_to_titles[url].append(title)
        
        # Check GitHub Repo specifically for opensource
        repo = item.get("github_repo")
        if repo:
            urls_to_check.add(repo)
            url_to_titles[repo].append(title)

    logger.info(f"Found {len(urls_to_check)} unique URLs to check.")

    broken_links: dict[str, dict] = {}
    
    # Use connector with a connection limit
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_url(session, url) for url in urls_to_check]
        
        # We can use asyncio.as_completed for progress indication if we wanted,
        # but gather is fine for this scale
        results = await asyncio.gather(*tasks)

        for url, is_valid, error in results:
            if not is_valid:
                broken_links[url] = {
                    "error": error,
                    "affected_items": url_to_titles[url]
                }
                logger.error(f"Broken Link: {url} -> {error}")
                if fail_fast:
                    return len(items), len(urls_to_check), 1, broken_links

    total = len(urls_to_check)
    broken_count = len(broken_links)
    
    return len(items), total, broken_count, broken_links


def generate_report(total_items: int, total: int, broken: int, broken_links: dict) -> str:
    """Generate a Markdown report card."""
    report = ["# 🔗 Link Validation Report Card", ""]
    report.append(f"**Total Database Items Scanned:** {total_items}")
    report.append(f"**Total Links Checked:** {total}")
    report.append(f"**Healthy Links:** {total - broken} ✅")
    report.append(f"**Broken Links:** {broken} " + ("❌" if broken > 0 else "✅"))
    report.append("")

    if broken > 0:
        report.append("## Broken Links Details")
        report.append("")
        for url, info in broken_links.items():
            report.append(f"### {url}")
            report.append(f"- **Error**: {info['error']}")
            report.append(f"- **Affected Items**: {', '.join(info['affected_items'])}")
            report.append("")
    
    return "\n".join(report)


def main():
    """CLI Entry point."""
    parser = argparse.ArgumentParser(description="Validate all external URLs in the database.")
    parser.add_argument("--fail-fast", action="store_true", help="Exit on the first broken link.")
    parser.add_argument("--output-report", type=str, help="Path to write the Markdown report card.")
    args = parser.parse_args()

    total_items, total, broken, broken_links = asyncio.run(main_async(args.fail_fast))

    if args.output_report:
        try:
            with open(args.output_report, "w", encoding="utf-8") as f:
                f.write(generate_report(total_items, total, broken, broken_links))
            logger.info(f"Report card written to {args.output_report}")
        except Exception as e:
            logger.error(f"Failed to write report: {e}")

    if broken > 0:
        logger.error(f"Failed: Found {broken} broken links out of {total} total links.")
        sys.exit(1)
    
    logger.info(f"Success: All {total} links are working correctly! ✅")
    sys.exit(0)


if __name__ == "__main__":
    main()
