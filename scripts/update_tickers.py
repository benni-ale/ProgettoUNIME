import requests
import json
import os

FMP_KEY = os.environ.get('FMP_KEY', 'qhgcRYfdz29EYiZXwLnKhugVrTYS0s0z')
url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={FMP_KEY}"

resp = requests.get(url)
data = resp.json()
tickers = [
    {"symbol": x["symbol"], "name": x.get("name", ""), "exchange": x.get("exchange", "")}
    for x in data[:500] if x.get("symbol") and x.get("name")
]

os.makedirs("static", exist_ok=True)
with open("static/tickers.json", "w", encoding="utf-8") as f:
    json.dump(tickers, f, ensure_ascii=False, indent=2)

print("Tickers salvati in static/tickers.json") 