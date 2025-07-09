# 🇮🇹 Provider di News Italiane

Questa applicazione ora supporta provider di news italiane per ottenere informazioni finanziarie locali.

## 📰 Provider Disponibili

### 1. **ANSA** (`ansa`)
- **Fonte**: Agenzia Nazionale Stampa Associata
- **Specializzazione**: News generali e finanziarie italiane
- **RSS Feed**: https://www.ansa.it/sito/ansait_rss.xml
- **Ideale per**: News generali su aziende italiane

### 2. **Il Sole 24 Ore** (`ilsole24ore`)
- **Fonte**: Quotidiano economico-finanziario
- **Specializzazione**: News finanziarie, economiche e di business
- **RSS Feed**: https://www.ilsole24ore.com/rss/home.xml
- **Ideale per**: Analisi finanziarie dettagliate

### 3. **La Repubblica** (`repubblica`)
- **Fonte**: Quotidiano nazionale
- **Specializzazione**: News generali con sezione economia
- **RSS Feed**: https://www.repubblica.it/rss/homepage/rss2.0.xml
- **Ideale per**: News generali su mercati italiani

### 4. **Corriere della Sera** (`corriere`)
- **Fonte**: Quotidiano nazionale
- **Specializzazione**: News generali e finanziarie
- **RSS Feed**: https://www.corriere.it/rss/homepage.xml
- **Ideale per**: Copertura generale del mercato

### 5. **Bloomberg Italia** (`bloomberg_italia`)
- **Fonte**: Bloomberg (contenuto internazionale)
- **Specializzazione**: News finanziarie globali
- **RSS Feed**: https://feeds.bloomberg.com/markets/news.rss
- **Ideale per**: News internazionali su aziende italiane

## 🚀 Come Utilizzare

### 1. **Avvia l'Applicazione**
```bash
python app.py
```

### 2. **Accedi all'Interfaccia Web**
- Apri il browser su `http://localhost:5000`
- Seleziona i ticker di interesse
- Scegli il provider italiano dal menu a tendina
- Clicca "🔍 Cerca News"

### 3. **Esempio di Ricerca**
```javascript
// Ricerca news su ENEL da ANSA
fetch('/search_ticker_news', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        tickers: ['ENEL'],
        days_back: 7,
        provider: 'ansa'
    })
})
```

## 🧪 Test dei Provider

Esegui il test automatico per verificare il funzionamento:

```bash
python test_italian_providers.py
```

Il test verificherà:
- ✅ Connessione al server
- ✅ Disponibilità dei provider
- ✅ Ricerca news per ogni provider
- ✅ Estrazione contenuto completo

## 📊 Vantaggi dei Provider Italiani

### **Rispetto a NewsAPI Internazionale**

| Caratteristica | Provider Italiani | NewsAPI |
|----------------|-------------------|---------|
| **Lingua** | 🇮🇹 Italiano nativo | 🌍 Multilingua |
| **Copertura** | Focus su mercato italiano | Globale |
| **Contenuto** | Dettagliato e contestualizzato | Generico |
| **Aggiornamenti** | Real-time | Con delay |
| **Costi** | Gratuito (RSS) | A pagamento |

### **Casi d'Uso Ideali**

#### **Provider Italiani**
- 📈 Analisi di mercato italiano
- 🏢 Due diligence su aziende italiane
- 📰 Monitoraggio media locali
- 🎓 Ricerca accademica su economia italiana

#### **NewsAPI**
- 🌍 Analisi globale
- 📊 Confronti internazionali
- 🔍 Ricerca multilingua
- 📈 Sentiment analysis globale

## 🔧 Configurazione Avanzata

### **Aggiungere Nuovi Provider**

1. **Aggiungi configurazione** in `app.py`:
```python
ITALIAN_NEWS_PROVIDERS = {
    'nuovo_provider': {
        'name': 'Nome Provider',
        'rss_url': 'https://provider.com/rss.xml',
        'search_url': 'https://provider.com/search',
        'base_url': 'https://provider.com'
    }
}
```

2. **Implementa metodo di ricerca**:
```python
def _search_nuovo_provider(self, query, days_back, max_results):
    # Logica di ricerca specifica
    pass
```

3. **Aggiungi al frontend**:
```html
<option value="nuovo_provider">Nome Provider</option>
```

### **Personalizzazione Query**

Ogni provider può avere query personalizzate:

```python
# ANSA - cerca anche termini italiani
query = f'"{ticker}" OR "{ticker} azioni" OR "{ticker} borsa"'

# Il Sole 24 Ore - focus su economia
query = f'"{ticker}" OR "{ticker} titoli" OR "{ticker} quotazione"'

# Bloomberg - internazionale
query = f'"{ticker}" OR "{ticker} stock" OR "{ticker} shares"'
```

## 📈 Esempi di Ricerca

### **Aziende Italiane Popolari**

| Ticker | Nome | Provider Consigliato |
|--------|------|---------------------|
| `ENEL` | Enel | ANSA, Il Sole 24 Ore |
| `ENI` | Eni | Il Sole 24 Ore, Bloomberg |
| `TIM` | Telecom Italia | La Repubblica, Corriere |
| `UCG` | UniCredit | Il Sole 24 Ore, Bloomberg |
| `RACE` | Ferrari | Bloomberg, ANSA |
| `ISP` | Intesa Sanpaolo | Il Sole 24 Ore, ANSA |

### **Query di Esempio**

```bash
# News su ENEL da ANSA
curl -X POST http://localhost:5000/search_ticker_news \
  -H "Content-Type: application/json" \
  -d '{"tickers":["ENEL"],"provider":"ansa","days_back":7}'

# News su ENI da Il Sole 24 Ore
curl -X POST http://localhost:5000/search_ticker_news \
  -H "Content-Type: application/json" \
  -d '{"tickers":["ENI"],"provider":"ilsole24ore","days_back":3}'
```

## 🛠️ Risoluzione Problemi

### **Errori Comuni**

1. **"Errore RSS"**
   - Verifica connessione internet
   - Controlla URL RSS feed
   - Provider potrebbe aver cambiato URL

2. **"Nessuna news trovata"**
   - Prova ticker diversi
   - Aumenta `days_back`
   - Cambia provider

3. **"Errore parsing articolo"**
   - Il sito potrebbe aver cambiato struttura
   - Usa fallback ai metadati RSS

### **Debug**

Abilita debug nel codice:
```python
print(f"[DEBUG] Query: {query}")
print(f"[DEBUG] Risultati: {len(results)}")
```

## 📝 Note Tecniche

- **Rate Limiting**: Pausa di 0.2s tra richieste per provider italiani
- **Fallback**: Se parsing fallisce, usa metadati RSS
- **Caching**: Risultati salvati in sessione utente
- **Estrazione**: Usa `newspaper3k` per contenuto completo

## 🔮 Sviluppi Futuri

- [ ] Sentiment analysis in italiano
- [ ] Più provider italiani (Milano Finanza, MF, etc.)
- [ ] Filtri per categoria news
- [ ] Notifiche real-time
- [ ] Export dati in Excel/CSV 