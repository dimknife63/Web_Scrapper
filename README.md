# Async Web Crawler

This is an asynchronous web crawler built in Python using `asyncio` and `aiohttp`. It can crawl a website concurrently, extract page data, and limit crawling based on maximum pages and concurrency.

---

## Features

- Crawls websites asynchronously with configurable concurrency.
- Extracts page data:
  - H1 headings
  - First paragraph
  - Outgoing links
  - Image URLs
- Respects a **maximum page limit** (`max_pages`) to prevent overloading.
- Avoids visiting the same page twice.
- Limits the number of simultaneous requests using a semaphore.

---

## Requirements

- Python 3.10+
- `aiohttp`
- `beautifulsoup4`

Install dependencies:

```bash
pip install aiohttp beautifulsoup4
