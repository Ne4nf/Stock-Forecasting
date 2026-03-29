import requests

def get_all_symbols():
    url = "https://cafef1.mediacdn.vn/Search/company.json"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()       # raise error if request failed
    
    data = resp.json()            # list of dicts
    symbols = [item["Symbol"] for item in data]
    return symbols

