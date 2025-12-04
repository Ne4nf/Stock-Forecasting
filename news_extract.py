# cafef_full_search_and_content.py
import requests
from bs4 import BeautifulSoup
import json
import time as time_module
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

def build_search_url(symbol: str, page: int = 1):
    """Generate correct search URL for any page."""
    if page == 1:
        return f"https://cafef.vn/tim-kiem.chn?keywords={quote_plus(symbol)}"
    return f"https://cafef.vn/tim-kiem/trang-{page}.chn?keywords={quote_plus(symbol)}"

def fetch_html(url: str, timeout=15, max_retries=3):
    for attempt in range(1, max_retries+1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except Exception:
            if attempt == max_retries:
                raise
            time_module.sleep(0.5 * attempt)

def extract_news_list(html: str):
    """Extract news items from search page."""
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for item in soup.find_all("div", class_="item"):
        title_tag = item.find("a", class_="item-title")
        if not title_tag:
            h3 = item.find("h3")
            if h3:
                title_tag = h3.find("a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag.get("href", "").strip()
        if href.startswith("/"):
            href = "https://cafef.vn" + href

        items.append({"title": title, "url": href})
    return items

def extract_article(url: str):
    """Extract publish time, sapo, content, author from article page."""
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # Publish Time
    t_tag = soup.find("span", class_="pdate")
    publish_time = t_tag.get_text(strip=True) if t_tag else None

    # Sapo
    sapo_tag = soup.find("h2", {"data-role": "sapo"})
    sapo = sapo_tag.get_text(strip=True) if sapo_tag else None

    # Content
    content_block = soup.find("div", {"data-role": "content"})
    content = ""
    if content_block:
        for p in content_block.find_all(["p", "figure"]):
            text = p.get_text(" ", strip=True)
            if text:
                content += text + "\n"

    # Author
    author_tag = soup.find("p", class_="author")
    author = author_tag.get_text(strip=True) if author_tag else None

    return {
        "time": publish_time,
        "sapo": sapo,
        "content": content.strip(),
        "author": author,
    }

def crawl_all_pages(symbol: str, out_file="output.jsonl"):
    results = []
    page = 1

    while True:
        search_url = build_search_url(symbol, page)
        print(f"[+] Fetching page {page}: {search_url}")

        html = fetch_html(search_url)
        items = extract_news_list(html)

        if not items:
            print(f"[!] Page {page} is empty → STOP.")
            break

        print(f"    Found {len(items)} news on page {page}")

        # For each news → fetch full content
        for idx, item in enumerate(items, 1):
            print(f"    [{idx}/{len(items)}] Crawling article: {item['url']}")
            try:
                article_data = extract_article(item["url"])
            except Exception as e:
                print("       [ERROR] Failed:", e)
                continue

            results.append({
                "title": item["title"],
                "url": item["url"],
                "time": article_data["time"],
                "sapo": article_data["sapo"],
                "content": article_data["content"],
                "author": article_data["author"],
            })

        page += 1

    # Write output
    with open(out_file, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("[✓] DONE! Saved all results to:", out_file)
    return results

# ---------------- MAIN ----------------
if __name__ == "__main__":
    symbol = "VJC"
    crawl_all_pages(symbol, out_file=f"news/{symbol}_all_news.jsonl")
