import requests
from urllib.parse import urlencode

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/ThongKeDL.ashx"


def fetch_cafef_history(
    symbol: str,
    start_date: str,
    end_date: str,
    page_index: int = 1,
    page_size: int = 20
):
    """
    Fetch historical stock data from CafeF.
    
    Args:
        symbol (str): Stock ticker (e.g., 'VJC')
        start_date (str): dd/mm/yyyy
        end_date (str): dd/mm/yyyy
        page_index (int): Page number
        page_size (int): Page size (default 20)
    
    Returns:
        dict: JSON data returned by CafeF API
    """

    params = {
        "Symbol": symbol,
        "StartDate": start_date,
        "EndDate": end_date,
        "PageIndex": page_index,
        "PageSize": page_size,
    }

    url = f"{BASE_URL}?{urlencode(params)}"
    print("[Request]", url)

    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    # CafeF returns raw JSON text
    return r.json()


# ----------------- EXAMPLE USAGE -----------------
if __name__ == "__main__":
    data = fetch_cafef_history(
        symbol="VJC",
        start_date="11/06/2025",
        end_date="12/04/2025",
        page_index=1,
        page_size=20
    )

    print(data)
