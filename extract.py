from request_stock_sticker import get_all_symbols
from news_extract import crawl_all_pages

symbols = get_all_symbols()
for symbol in symbols:
    out_file = f"news/{symbol}.jsonl"
    crawl_all_pages(symbol, out_file=out_file)