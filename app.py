from flask import Flask, render_template, request, jsonify, session
from newsapi import NewsApiClient
from newspaper import Article
import os
import requests
import json
from datetime import datetime
import time
import uuid

app = Flask(__name__)

# Chiave segreta per le sessioni (in produzione usare una chiave sicura)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Inserisci qui la tua API key di NewsAPI
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY', '10aa975f0e0a4a259223fab52d03d8d8')
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# Chiave Financial Modeling Prep
FMP_KEY = os.environ.get('FMP_KEY', 'qhgcRYfdz29EYiZXwLnKhugVrTYS0s0z')

def get_user_id():
    """Genera o recupera l'ID utente per la sessione"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def get_user_news():
    """Recupera le news dell'utente dalla sessione"""
    user_id = get_user_id()
    if 'saved_news' not in session:
        session['saved_news'] = []
    return session['saved_news']

def save_user_news(news_data):
    """Salva le news dell'utente nella sessione"""
    user_news = get_user_news()
    
    # Aggiungi timestamp e user_id
    news_data['timestamp'] = datetime.now().isoformat()
    news_data['user_id'] = get_user_id()
    
    # Aggiungi alla lista
    user_news.append(news_data)
    
    # Mantieni solo le ultime 20 ricerche per sessione
    if len(user_news) > 20:
        user_news = user_news[-20:]
    
    session['saved_news'] = user_news
    session.modified = True
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tickers')
def tickers():
    """Carica i ticker dal file JSON locale"""
    try:
        with open('static/tickers.json', 'r', encoding='utf-8') as f:
            tickers = json.load(f)
        return jsonify(tickers)
    except Exception as e:
        print(f"Errore nel caricamento tickers: {e}")
        return jsonify([])

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

@app.route('/search_ticker_news', methods=['POST'])
def search_ticker_news():
    """Cerca news per uno o più ticker specifici"""
    data = request.json
    tickers = data.get('tickers', [])
    days_back = data.get('days_back', 7)  # Default: ultimi 7 giorni
    
    if not tickers:
        return jsonify({'error': 'Nessun ticker specificato'}), 400
    
    all_results = []
    
    for ticker in tickers:
        try:
            # Cerca news per il ticker
            query = f'"{ticker}" OR "{ticker} stock" OR "{ticker} shares"'
            articles = newsapi.get_everything(
                q=query,
                language='en',
                sort_by='publishedAt',
                from_param=f'{days_back} days ago',
                page_size=10
            )
            
            ticker_results = []
            for art in articles.get('articles', []):
                try:
                    # Estrai contenuto completo se possibile
                    url = art['url']
                    article = Article(url)
                    article.download()
                    article.parse()
                    
                    ticker_results.append({
                        'ticker': ticker,
                        'title': article.title or art['title'],
                        'url': url,
                        'source': art['source']['name'],
                        'publishedAt': art['publishedAt'],
                        'description': art.get('description', ''),
                        'text': article.text[:1000] + '...' if article.text else '',
                        'sentiment': 'neutral'  # Placeholder per sentiment analysis
                    })
                except Exception as e:
                    # Se non riesce a scaricare l'articolo, usa i dati base
                    ticker_results.append({
                        'ticker': ticker,
                        'title': art['title'],
                        'url': url,
                        'source': art['source']['name'],
                        'publishedAt': art['publishedAt'],
                        'description': art.get('description', ''),
                        'text': art.get('content', '')[:500] + '...' if art.get('content') else '',
                        'sentiment': 'neutral'
                    })
            
            all_results.extend(ticker_results)
            
            # Pausa per evitare rate limiting
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Errore nella ricerca news per {ticker}: {e}")
            continue
    
    # Salva i risultati nella sessione dell'utente
    if all_results:
        save_user_news({
            'tickers': tickers,
            'days_back': days_back,
            'total_articles': len(all_results),
            'articles': all_results
        })
    
    return jsonify({
        'success': True,
        'total_articles': len(all_results),
        'articles': all_results,
        'user_id': get_user_id()
    })

@app.route('/saved_news')
def get_saved_news():
    """Restituisce le news salvate dell'utente"""
    user_news = get_user_news()
    return jsonify({
        'news': user_news,
        'user_id': get_user_id(),
        'total_searches': len(user_news)
    })

@app.route('/clear_news', methods=['POST'])
def clear_news():
    """Cancella tutte le news salvate dell'utente"""
    try:
        session['saved_news'] = []
        session.modified = True
        return jsonify({
            'success': True, 
            'message': 'News cancellate con successo',
            'user_id': get_user_id()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user_info')
def user_info():
    """Restituisce informazioni sull'utente"""
    user_news = get_user_news()
    return jsonify({
        'user_id': get_user_id(),
        'total_searches': len(user_news),
        'session_active': True
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)