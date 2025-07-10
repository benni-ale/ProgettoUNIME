from flask import Flask, render_template, request, jsonify, session
from newsapi import NewsApiClient
from newspaper import Article
import os
import requests
import json
from datetime import datetime
import time
import uuid
import feedparser
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Chiave segreta per le sessioni (in produzione usare una chiave sicura)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Inserisci qui la tua API key di NewsAPI
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY', '10aa975f0e0a4a259223fab52d03d8d8')
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# Chiave Financial Modeling Prep
FMP_KEY = os.environ.get('FMP_KEY', 'qhgcRYfdz29EYiZXwLnKhugVrTYS0s0z')

# Provider di news italiane
ITALIAN_NEWS_PROVIDERS = {
    'ansa': {
        'name': 'ANSA',
        'rss_url': 'https://www.ansa.it/sito/ansait_rss.xml',
        'search_url': 'https://www.ansa.it/sito/search.html',
        'base_url': 'https://www.ansa.it'
    },
    'ilsole24ore': {
        'name': 'Il Sole 24 Ore',
        'rss_url': 'https://www.ilsole24ore.com/rss/home.xml',
        'search_url': 'https://www.ilsole24ore.com/search',
        'base_url': 'https://www.ilsole24ore.com'
    },
    'repubblica': {
        'name': 'La Repubblica',
        'rss_url': 'https://www.repubblica.it/rss/homepage/rss2.0.xml',
        'search_url': 'https://www.repubblica.it/search',
        'base_url': 'https://www.repubblica.it'
    },
    'corriere': {
        'name': 'Corriere della Sera',
        'rss_url': 'https://www.corriere.it/rss/homepage.xml',
        'search_url': 'https://www.corriere.it/search',
        'base_url': 'https://www.corriere.it'
    },
    'bloomberg_italia': {
        'name': 'Bloomberg Italia',
        'rss_url': 'https://feeds.bloomberg.com/markets/news.rss',
        'search_url': 'https://www.bloomberg.com/search',
        'base_url': 'https://www.bloomberg.com'
    }
}

# Lista di ticker italiani noti (puoi espandere questa lista)
ITALIAN_TICKERS = [
    'ENEL', 'ENI', 'ISP', 'UCG', 'STM', 'ATL', 'G', 'SRG', 'TEN', 'TRN', 'BMED', 'BAMI', 'MB', 'BMPS', 'BZU', 'CPR', 'DIA', 'F', 'FBK', 'JUVE', 'LDO', 'MONC', 'PIRC', 'PRY', 'RACE', 'REC', 'SFER', 'TIT', 'UNI', 'BZU', 'IGD', 'CASS', 'CARR', 'CNHI', 'EXO', 'FCA', 'FERR', 'FNM', 'IGD', 'INW', 'IP', 'IT', 'LUX', 'MED', 'PST', 'SNA', 'SPM', 'UCG', 'UNI', 'VIV', 'BPE', 'BPSO', 'BPER', 'BPM', 'BAMI', 'BMPS', 'BZU', 'CASS', 'CARR', 'CNHI', 'EXO', 'FCA', 'FERR', 'FNM', 'IGD', 'INW', 'IP', 'IT', 'LUX', 'MED', 'PST', 'SNA', 'SPM', 'UCG', 'UNI', 'VIV'
]

class ItalianNewsProvider:
    """Provider per news italiane"""
    
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.config = ITALIAN_NEWS_PROVIDERS.get(provider_name, {})
    
    def search_news(self, query, days_back=7, max_results=10):
        """Cerca news per query specifica"""
        results = []
        
        try:
            if self.provider_name == 'ansa':
                results = self._search_ansa(query, days_back, max_results)
            elif self.provider_name == 'ilsole24ore':
                results = self._search_ilsole24ore(query, days_back, max_results)
            elif self.provider_name == 'repubblica':
                results = self._search_repubblica(query, days_back, max_results)
            elif self.provider_name == 'corriere':
                results = self._search_corriere(query, days_back, max_results)
            elif self.provider_name == 'bloomberg_italia':
                results = self._search_bloomberg(query, days_back, max_results)
            
        except Exception as e:
            print(f"Errore nel provider {self.provider_name}: {e}")
        
        return results
    
    def _search_ansa(self, query, days_back, max_results):
        """Ricerca specifica per ANSA"""
        results = []
        
        # Usa RSS feed di ANSA
        try:
            feed = feedparser.parse(self.config['rss_url'])
            
            for entry in feed.entries[:max_results]:
                # Controlla se la query è nel titolo o descrizione
                if (query.lower() in entry.title.lower() or 
                    query.lower() in entry.get('summary', '').lower()):
                    
                    try:
                        # Estrai contenuto completo
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        
                        results.append({
                            'title': article.title or entry.title,
                            'url': entry.link,
                            'source': 'ANSA',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': article.text[:1000] + '...' if article.text else '',
                            'sentiment': 'neutral'
                        })
                    except Exception as e:
                        # Fallback ai metadati RSS
                        results.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': 'ANSA',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': entry.get('summary', '')[:500] + '...',
                            'sentiment': 'neutral'
                        })
                        
        except Exception as e:
            print(f"Errore RSS ANSA: {e}")
        
        return results
    
    def _search_ilsole24ore(self, query, days_back, max_results):
        """Ricerca specifica per Il Sole 24 Ore"""
        results = []
        
        try:
            feed = feedparser.parse(self.config['rss_url'])
            
            for entry in feed.entries[:max_results]:
                if (query.lower() in entry.title.lower() or 
                    query.lower() in entry.get('summary', '').lower()):
                    
                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        
                        results.append({
                            'title': article.title or entry.title,
                            'url': entry.link,
                            'source': 'Il Sole 24 Ore',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': article.text[:1000] + '...' if article.text else '',
                            'sentiment': 'neutral'
                        })
                    except Exception as e:
                        results.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': 'Il Sole 24 Ore',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': entry.get('summary', '')[:500] + '...',
                            'sentiment': 'neutral'
                        })
                        
        except Exception as e:
            print(f"Errore RSS Il Sole 24 Ore: {e}")
        
        return results
    
    def _search_repubblica(self, query, days_back, max_results):
        """Ricerca specifica per La Repubblica"""
        results = []
        
        try:
            feed = feedparser.parse(self.config['rss_url'])
            
            for entry in feed.entries[:max_results]:
                if (query.lower() in entry.title.lower() or 
                    query.lower() in entry.get('summary', '').lower()):
                    
                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        
                        results.append({
                            'title': article.title or entry.title,
                            'url': entry.link,
                            'source': 'La Repubblica',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': article.text[:1000] + '...' if article.text else '',
                            'sentiment': 'neutral'
                        })
                    except Exception as e:
                        results.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': 'La Repubblica',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': entry.get('summary', '')[:500] + '...',
                            'sentiment': 'neutral'
                        })
                        
        except Exception as e:
            print(f"Errore RSS La Repubblica: {e}")
        
        return results
    
    def _search_corriere(self, query, days_back, max_results):
        """Ricerca specifica per Corriere della Sera"""
        results = []
        
        try:
            feed = feedparser.parse(self.config['rss_url'])
            
            for entry in feed.entries[:max_results]:
                if (query.lower() in entry.title.lower() or 
                    query.lower() in entry.get('summary', '').lower()):
                    
                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        
                        results.append({
                            'title': article.title or entry.title,
                            'url': entry.link,
                            'source': 'Corriere della Sera',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': article.text[:1000] + '...' if article.text else '',
                            'sentiment': 'neutral'
                        })
                    except Exception as e:
                        results.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': 'Corriere della Sera',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': entry.get('summary', '')[:500] + '...',
                            'sentiment': 'neutral'
                        })
                        
        except Exception as e:
            print(f"Errore RSS Corriere: {e}")
        
        return results
    
    def _search_bloomberg(self, query, days_back, max_results):
        """Ricerca specifica per Bloomberg Italia"""
        results = []
        
        try:
            feed = feedparser.parse(self.config['rss_url'])
            
            for entry in feed.entries[:max_results]:
                # Bloomberg ha spesso contenuto in inglese, cerca anche traduzioni italiane
                if (query.lower() in entry.title.lower() or 
                    query.lower() in entry.get('summary', '').lower()):
                    
                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        
                        results.append({
                            'title': article.title or entry.title,
                            'url': entry.link,
                            'source': 'Bloomberg',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': article.text[:1000] + '...' if article.text else '',
                            'sentiment': 'neutral'
                        })
                    except Exception as e:
                        results.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': 'Bloomberg',
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'description': entry.get('summary', ''),
                            'text': entry.get('summary', '')[:500] + '...',
                            'sentiment': 'neutral'
                        })
                        
        except Exception as e:
            print(f"Errore RSS Bloomberg: {e}")
        
        return results

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

@app.route('/italian_providers')
def italian_providers():
    """Restituisce la lista dei provider italiani disponibili"""
    return jsonify(list(ITALIAN_NEWS_PROVIDERS.keys()))

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    category = data.get('category')
    source = data.get('source')
    provider = data.get('provider', 'newsapi')  # Nuovo parametro
    
    if provider in ITALIAN_NEWS_PROVIDERS:
        # Usa provider italiano
        italian_provider = ItalianNewsProvider(provider)
        results = italian_provider.search_news(query, days_back=7, max_results=10)
    else:
        # Usa NewsAPI (default)
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
    provider = data.get('provider', 'newsapi')  # Nuovo parametro
    providers = data.get('providers', [])  # Nuovo parametro per selezione multipla

    if not tickers:
        return jsonify({'error': 'Nessun ticker specificato'}), 400

    # Gestione provider multipli
    if providers and isinstance(providers, list):
        # Se sono specificati provider multipli, usa quelli
        selected_providers = providers
    elif provider in ITALIAN_NEWS_PROVIDERS:
        # Se è specificato un singolo provider italiano, usa quello
        selected_providers = [provider]
    else:
        # Default: usa NewsAPI
        selected_providers = ['newsapi']

    # Filtro: provider italiano e ticker non italiano
    italian_providers_selected = [p for p in selected_providers if p in ITALIAN_NEWS_PROVIDERS]
    if italian_providers_selected:
        non_italian = [t for t in tickers if t.upper() not in ITALIAN_TICKERS]
        if non_italian:
            return jsonify({
                'success': False,
                'error': 'I provider italiani supportano solo aziende italiane. Seleziona solo ticker italiani come ENEL, ENI, ISP, UCG, STM, ATL, ecc.',
                'invalid_tickers': non_italian,
                'hint': 'Per aziende estere usa NewsAPI (Internazionale) come provider.'
            }), 400

    all_results = []
    
    # Gestione provider italiani multipli
    if italian_providers_selected:
        for provider_name in italian_providers_selected:
            italian_provider = ItalianNewsProvider(provider_name)
            
            for ticker in tickers:
                try:
                    # Cerca news italiane per il ticker
                    ticker_results = italian_provider.search_news(
                        f'"{ticker}" OR "{ticker} azioni" OR "{ticker} borsa"', 
                        days_back, 
                        max_results=5
                    )
                    
                    # Aggiungi ticker e provider a ogni risultato
                    for result in ticker_results:
                        result['ticker'] = ticker
                        result['provider'] = provider_name
                    
                    all_results.extend(ticker_results)
                    
                    # Pausa per evitare rate limiting
                    time.sleep(0.2)
                    
                except Exception as e:
                    print(f"[DEBUG] Errore nella ricerca news italiane per {ticker} su {provider_name}: {e}")
                    continue
    else:
        # Usa NewsAPI (logica esistente)
        from datetime import datetime, timedelta
        from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        print(f"[DEBUG] Cerco news per tickers: {tickers} dal {from_date}")
        
        for ticker in tickers:
            try:
                # Cerca news per il ticker
                query = f'"{ticker}" OR "{ticker} stock" OR "{ticker} shares"'
                print(f"[DEBUG] Query NewsAPI: {query}")
                articles = newsapi.get_everything(
                    q=query,
                    language='en',
                    sort_by='publishedAt',
                    from_param=from_date,
                    page_size=10
                )
                print(f"[DEBUG] Risposta NewsAPI per {ticker}: {json.dumps(articles)[:500]}")
                
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
                        print(f"[DEBUG] Errore parsing articolo {url}: {e}")
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
                print(f"[DEBUG] Errore nella ricerca news per {ticker}: {e}")
                continue
    
    # Salva i risultati nella sessione dell'utente
    if all_results:
        save_user_news({
            'tickers': tickers,
            'days_back': days_back,
            'total_articles': len(all_results),
            'articles': all_results,
            'providers': selected_providers
        })
    
    print(f"[DEBUG] Totale articoli trovati: {len(all_results)} da {len(selected_providers)} provider")
    return jsonify({
        'success': True,
        'total_articles': len(all_results),
        'articles': all_results,
        'user_id': get_user_id(),
        'providers': selected_providers,
        'provider': selected_providers[0] if selected_providers else 'newsapi'  # Per compatibilità
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