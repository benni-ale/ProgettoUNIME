import requests
import json
import os
import sys

def get_fallback_tickers():
    """Fallback list of major S&P 500 stocks if API fails"""
    return [
        {"symbol": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "exchange": "NASDAQ"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "exchange": "NASDAQ"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "exchange": "NASDAQ"},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "exchange": "NASDAQ"},
        {"symbol": "TSLA", "name": "Tesla Inc.", "exchange": "NASDAQ"},
        {"symbol": "META", "name": "Meta Platforms Inc.", "exchange": "NASDAQ"},
        {"symbol": "BRK.A", "name": "Berkshire Hathaway Inc.", "exchange": "NYSE"},
        {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "exchange": "NYSE"},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "exchange": "NYSE"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "exchange": "NYSE"},
        {"symbol": "V", "name": "Visa Inc.", "exchange": "NYSE"},
        {"symbol": "PG", "name": "Procter & Gamble Co.", "exchange": "NYSE"},
        {"symbol": "HD", "name": "Home Depot Inc.", "exchange": "NYSE"},
        {"symbol": "MA", "name": "Mastercard Inc.", "exchange": "NYSE"},
        {"symbol": "DIS", "name": "Walt Disney Co.", "exchange": "NYSE"},
        {"symbol": "PYPL", "name": "PayPal Holdings Inc.", "exchange": "NASDAQ"},
        {"symbol": "ADBE", "name": "Adobe Inc.", "exchange": "NASDAQ"},
        {"symbol": "NFLX", "name": "Netflix Inc.", "exchange": "NASDAQ"},
        {"symbol": "CRM", "name": "Salesforce Inc.", "exchange": "NYSE"},
        {"symbol": "ABBV", "name": "AbbVie Inc.", "exchange": "NYSE"},
        {"symbol": "PFE", "name": "Pfizer Inc.", "exchange": "NYSE"},
        {"symbol": "KO", "name": "Coca-Cola Co.", "exchange": "NYSE"},
        {"symbol": "PEP", "name": "PepsiCo Inc.", "exchange": "NASDAQ"},
        {"symbol": "AVGO", "name": "Broadcom Inc.", "exchange": "NASDAQ"},
        {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc.", "exchange": "NYSE"},
        {"symbol": "COST", "name": "Costco Wholesale Corp.", "exchange": "NASDAQ"},
        {"symbol": "ABT", "name": "Abbott Laboratories", "exchange": "NYSE"},
        {"symbol": "DHR", "name": "Danaher Corp.", "exchange": "NYSE"},
        {"symbol": "VZ", "name": "Verizon Communications Inc.", "exchange": "NYSE"},
        {"symbol": "ACN", "name": "Accenture Plc", "exchange": "NYSE"},
        {"symbol": "WMT", "name": "Walmart Inc.", "exchange": "NYSE"},
        {"symbol": "LLY", "name": "Eli Lilly and Co.", "exchange": "NYSE"},
        {"symbol": "TXN", "name": "Texas Instruments Inc.", "exchange": "NASDAQ"},
        {"symbol": "QCOM", "name": "Qualcomm Inc.", "exchange": "NASDAQ"},
        {"symbol": "HON", "name": "Honeywell International Inc.", "exchange": "NASDAQ"},
        {"symbol": "NKE", "name": "Nike Inc.", "exchange": "NYSE"},
        {"symbol": "PM", "name": "Philip Morris International Inc.", "exchange": "NYSE"},
        {"symbol": "LOW", "name": "Lowe's Companies Inc.", "exchange": "NYSE"},
        {"symbol": "INTC", "name": "Intel Corp.", "exchange": "NASDAQ"},
        {"symbol": "UNP", "name": "Union Pacific Corp.", "exchange": "NYSE"},
        {"symbol": "IBM", "name": "International Business Machines Corp.", "exchange": "NYSE"},
        {"symbol": "CAT", "name": "Caterpillar Inc.", "exchange": "NYSE"},
        {"symbol": "UPS", "name": "United Parcel Service Inc.", "exchange": "NYSE"},
        {"symbol": "MS", "name": "Morgan Stanley", "exchange": "NYSE"},
        {"symbol": "RTX", "name": "Raytheon Technologies Corp.", "exchange": "NYSE"},
        {"symbol": "SPGI", "name": "S&P Global Inc.", "exchange": "NYSE"},
        {"symbol": "GS", "name": "Goldman Sachs Group Inc.", "exchange": "NYSE"},
        {"symbol": "AMAT", "name": "Applied Materials Inc.", "exchange": "NASDAQ"},
        {"symbol": "ISRG", "name": "Intuitive Surgical Inc.", "exchange": "NASDAQ"},
        {"symbol": "PLD", "name": "Prologis Inc.", "exchange": "NYSE"},
        {"symbol": "T", "name": "AT&T Inc.", "exchange": "NYSE"},
        {"symbol": "DE", "name": "Deere & Co.", "exchange": "NYSE"},
        {"symbol": "GILD", "name": "Gilead Sciences Inc.", "exchange": "NASDAQ"},
        {"symbol": "LMT", "name": "Lockheed Martin Corp.", "exchange": "NYSE"},
        {"symbol": "AMGN", "name": "Amgen Inc.", "exchange": "NASDAQ"},
        {"symbol": "ADI", "name": "Analog Devices Inc.", "exchange": "NASDAQ"},
        {"symbol": "BKNG", "name": "Booking Holdings Inc.", "exchange": "NASDAQ"},
        {"symbol": "MDLZ", "name": "Mondelez International Inc.", "exchange": "NASDAQ"},
        {"symbol": "GE", "name": "General Electric Co.", "exchange": "NYSE"},
        {"symbol": "REGN", "name": "Regeneron Pharmaceuticals Inc.", "exchange": "NASDAQ"},
        {"symbol": "CMCSA", "name": "Comcast Corp.", "exchange": "NASDAQ"},
        {"symbol": "TMUS", "name": "T-Mobile US Inc.", "exchange": "NASDAQ"},
        {"symbol": "INTU", "name": "Intuit Inc.", "exchange": "NASDAQ"},
        {"symbol": "AMT", "name": "American Tower Corp.", "exchange": "NYSE"},
        {"symbol": "ADP", "name": "Automatic Data Processing Inc.", "exchange": "NASDAQ"},
        {"symbol": "CB", "name": "Chubb Ltd.", "exchange": "NYSE"},
        {"symbol": "BDX", "name": "Becton Dickinson and Co.", "exchange": "NYSE"},
        {"symbol": "SO", "name": "Southern Co.", "exchange": "NYSE"},
        {"symbol": "DUK", "name": "Duke Energy Corp.", "exchange": "NYSE"},
        {"symbol": "ITW", "name": "Illinois Tool Works Inc.", "exchange": "NYSE"},
        {"symbol": "CME", "name": "CME Group Inc.", "exchange": "NASDAQ"},
        {"symbol": "CSCO", "name": "Cisco Systems Inc.", "exchange": "NASDAQ"},
        {"symbol": "BLK", "name": "BlackRock Inc.", "exchange": "NYSE"},
        {"symbol": "SCHW", "name": "Charles Schwab Corp.", "exchange": "NYSE"},
        {"symbol": "CI", "name": "Cigna Corp.", "exchange": "NYSE"},
        {"symbol": "TJX", "name": "TJX Companies Inc.", "exchange": "NYSE"},
        {"symbol": "AXP", "name": "American Express Co.", "exchange": "NYSE"},
        {"symbol": "USB", "name": "U.S. Bancorp", "exchange": "NYSE"},
        {"symbol": "PGR", "name": "Progressive Corp.", "exchange": "NYSE"},
        {"symbol": "TRV", "name": "Travelers Companies Inc.", "exchange": "NYSE"},
        {"symbol": "MMC", "name": "Marsh & McLennan Companies Inc.", "exchange": "NYSE"},
        {"symbol": "ETN", "name": "Eaton Corp. Plc", "exchange": "NYSE"},
        {"symbol": "SLB", "name": "Schlumberger Ltd.", "exchange": "NYSE"},
        {"symbol": "FISV", "name": "Fiserv Inc.", "exchange": "NASDAQ"},
        {"symbol": "ICE", "name": "Intercontinental Exchange Inc.", "exchange": "NYSE"},
        {"symbol": "AON", "name": "Aon Plc", "exchange": "NYSE"},
        {"symbol": "SYK", "name": "Stryker Corp.", "exchange": "NYSE"},
        {"symbol": "KLAC", "name": "KLA Corp.", "exchange": "NASDAQ"},
        {"symbol": "HUM", "name": "Humana Inc.", "exchange": "NYSE"},
        {"symbol": "APD", "name": "Air Products and Chemicals Inc.", "exchange": "NYSE"},
        {"symbol": "SHW", "name": "Sherwin-Williams Co.", "exchange": "NYSE"},
        {"symbol": "ECL", "name": "Ecolab Inc.", "exchange": "NYSE"},
        {"symbol": "MCD", "name": "McDonald's Corp.", "exchange": "NYSE"},
        {"symbol": "NEE", "name": "NextEra Energy Inc.", "exchange": "NYSE"},
        {"symbol": "COP", "name": "ConocoPhillips", "exchange": "NYSE"},
        {"symbol": "EOG", "name": "EOG Resources Inc.", "exchange": "NYSE"},
        {"symbol": "CVX", "name": "Chevron Corp.", "exchange": "NYSE"},
        {"symbol": "XOM", "name": "Exxon Mobil Corp.", "exchange": "NYSE"}
    ]

def update_tickers():
    FMP_KEY = os.environ.get('FMP_KEY', 'qhgcRYfdz29EYiZXwLnKhugVrTYS0s0z')
    url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_KEY}"
    
    print(f"Fetching S&P 500 constituents from: {url}")
    
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        
        data = resp.json()
        print(f"API Response type: {type(data)}")
        print(f"API Response length: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"First item: {data[0]}")
        else:
            print(f"Full response: {data}")
        
        if not isinstance(data, list):
            print(f"Error: Expected list but got {type(data)}")
            print(f"Response content: {data}")
            return False
        
        tickers = []
        for x in data:
            if isinstance(x, dict):
                symbol = x.get("symbol")
                name = x.get("name", "")
                exchange = x.get("exchange", "")
                
                if symbol and name:
                    tickers.append({
                        "symbol": symbol,
                        "name": name,
                        "exchange": exchange
                    })
            else:
                print(f"Warning: Skipping non-dict item: {x}")
        
        tickers = sorted(tickers, key=lambda x: x["symbol"])
        
        os.makedirs("static", exist_ok=True)
        
        with open("static/tickers.json", "w", encoding="utf-8") as f:
            json.dump(tickers, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully saved {len(tickers)} S&P 500 tickers to static/tickers.json")
        print(f"Sample tickers: {tickers[:5]}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("🔄 Using fallback ticker list...")
        return use_fallback_tickers()
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print("🔄 Using fallback ticker list...")
        return use_fallback_tickers()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("🔄 Using fallback ticker list...")
        return use_fallback_tickers()

def use_fallback_tickers():
    """Use fallback ticker list when API fails"""
    tickers = get_fallback_tickers()
    
    os.makedirs("static", exist_ok=True)
    
    with open("static/tickers.json", "w", encoding="utf-8") as f:
        json.dump(tickers, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(tickers)} fallback tickers to static/tickers.json")
    print(f"Sample tickers: {tickers[:5]}")
    return True

if __name__ == "__main__":
    success = update_tickers()
    if not success:
        sys.exit(1) 