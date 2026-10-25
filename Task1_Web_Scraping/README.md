# Task 1 — Web Scraping

## Goal
Use `requests` and `BeautifulSoup` to collect book title, price, rating, availability, and category from the public practice site `books.toscrape.com`.

## Run
From the main folder:
```bash
python Task1_Web_Scraping/scrape_books.py
```

The script follows the site's pagination and saves `output/books_scraped.csv`. It limits the number of pages by default so the task is quick to run. You can change `MAX_PAGES` in the script.

## What to explain
- `requests.get()` downloads a page.
- `BeautifulSoup` reads the HTML.
- CSS selectors find book cards and their fields.
- The loop follows the “next” page.
- pandas saves the collected rows as CSV.

This is a practice website designed for scraping exercises. Keep requests polite and do not use this script against websites that prohibit scraping.
