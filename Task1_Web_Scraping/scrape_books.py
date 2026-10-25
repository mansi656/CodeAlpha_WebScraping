from pathlib import Path
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
MAX_PAGES = 5  # Increase carefully if you need more practice data.
OUTPUT_FILE = Path(__file__).resolve().parent / "output" / "books_scraped.csv"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def scrape_books():
    rows = []
    next_url = BASE_URL
    session = requests.Session()
    session.headers.update({"User-Agent": "EducationalDataAnalyticsProject/1.0 (student practice)"})

    for page_number in range(1, MAX_PAGES + 1):
        print(f"Reading page {page_number}: {next_url}")
        response = session.get(next_url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for card in soup.select("article.product_pod"):
            title = card.h3.a.get("title", "").strip()
            relative_link = card.h3.a.get("href", "")
            product_url = urljoin(next_url, relative_link)
            price_text = card.select_one(".price_color").get_text(strip=True)
            price = float(price_text.replace("£", "").replace("Â", ""))
            rating_classes = card.select_one("p.star-rating").get("class", [])
            rating_word = next((c for c in rating_classes if c in RATING_MAP), "")
            availability = card.select_one(".availability").get_text(" ", strip=True)

            # The category is on each product page; visit it to collect the field.
            product_response = session.get(product_url, timeout=20)
            product_response.raise_for_status()
            product_soup = BeautifulSoup(product_response.text, "html.parser")
            breadcrumbs = product_soup.select("ul.breadcrumb li a")
            category = breadcrumbs[-1].get_text(strip=True) if len(breadcrumbs) >= 2 else "Unknown"

            rows.append({
                "title": title,
                "price_gbp": price,
                "rating": RATING_MAP.get(rating_word),
                "availability": "In stock" if "In stock" in availability else availability,
                "category": category,
                "product_url": product_url,
            })
            time.sleep(0.15)  # Small pause between product requests.

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        next_url = urljoin(next_url, next_link.get("href", ""))
        time.sleep(0.3)

    if not rows:
        raise RuntimeError("No books were collected. Check your internet connection or try again later.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows).drop_duplicates(subset=["title"])
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\nDone! Saved {len(df)} books to:\n{OUTPUT_FILE}")
    print(df.head().to_string(index=False))

if __name__ == "__main__":
    try:
        scrape_books()
    except requests.RequestException as exc:
        print(f"Network error: {exc}")
        print("Check your internet connection and run the script again.")
    except Exception as exc:
        print(f"Scraping stopped: {exc}")
