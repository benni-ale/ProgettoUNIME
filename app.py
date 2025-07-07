from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient
from newspaper import Article
import os
import requests

app = Flask(__name__)

# Inserisci qui la tua API key di NewsAPI
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY', '10aa975f0e0a4a259223fab52d03d8d8')
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# Chiave Financial Modeling Prep
FMP_KEY = os.environ.get('FMP_KEY', 'qhgcRYfdz29EYiZXwLnKhugVrTYS0s0z')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tickers')
def tickers():
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={FMP_KEY}'
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        # Prendi solo i primi 500 ticker e solo symbol, name, exchange
        tickers = [{
            'symbol': x['symbol'],
            'name': x.get('name', ''),
            'exchange': x.get('exchange', '')
        } for x in data[:500] if x.get('symbol') and x.get('name')]
        return jsonify(tickers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    category = data.get('category')
    source = data.get('source')
    if source:
        articles = newsapi.get_top_headlines(q=query, language='it', page_size=5, sources=source)
    elif category:
        articles = newsapi.get_top_headlines(q=query, language='it', page_size=5, category=category)
    else:
        articles = newsapi.get_everything(q=query, language='it', page_size=5)
    results = []
    for art in articles['articles']:
        url = art['url']
        try:
            article = Article(url)
            article.download()
            article.parse()
            results.append({
                'title': article.title or art['title'],
                'url': url,
                'source': art['source']['name'],
                'publishedAt': art['publishedAt'],
                'text': article.text[:500] + '...' if article.text else '',
            })
        except Exception as e:
            results.append({'title': art['title'], 'url': url, 'error': str(e)})
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)