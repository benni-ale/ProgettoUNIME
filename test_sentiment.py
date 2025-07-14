#!/usr/bin/env python3
"""
Test script per verificare il funzionamento del sentiment analysis con FinBERT
"""

import requests
import json
import time

def test_sentiment_analysis():
    """Testa l'analisi del sentiment"""
    base_url = "http://localhost:5000"
    
    print("🧪 Test Sentiment Analysis con FinBERT")
    print("=" * 50)
    
    # Test 1: Analisi sentiment di un testo singolo
    print("\n1️⃣ Test analisi sentiment singola...")
    test_text = "Apple reported strong quarterly earnings with revenue growth of 15%"
    
    try:
        response = requests.post(f"{base_url}/analyze_sentiment", 
                               json={"text": test_text},
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successo!")
            print(f"   Testo: {test_text}")
            print(f"   Sentiment: {result.get('sentiment', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            print(f"   Scores: {result.get('scores', 'N/A')}")
        else:
            print(f"❌ Errore: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
    
    # Test 2: Statistiche sentiment
    print("\n2️⃣ Test statistiche sentiment...")
    try:
        response = requests.get(f"{base_url}/get_sentiment_statistics")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successo!")
            print(f"   Statistiche: {result.get('statistics', 'N/A')}")
            print(f"   Totale articoli: {result.get('total_articles', 'N/A')}")
        else:
            print(f"❌ Errore: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
    
    # Test 3: Analisi sentiment news salvate
    print("\n3️⃣ Test analisi sentiment news salvate...")
    try:
        response = requests.post(f"{base_url}/analyze_saved_news_sentiment",
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successo!")
            print(f"   Messaggio: {result.get('message', 'N/A')}")
            print(f"   Articoli analizzati: {result.get('articles_analyzed', 'N/A')}")
            print(f"   Statistiche: {result.get('statistics', 'N/A')}")
        elif response.status_code == 404:
            print("ℹ️ Nessuna news salvata trovata (normale se non ci sono ricerche salvate)")
        else:
            print(f"❌ Errore: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
    
    # Test 4: Filtro per sentiment
    print("\n4️⃣ Test filtro per sentiment...")
    try:
        response = requests.post(f"{base_url}/filter_news_by_sentiment",
                               json={"sentiment": "positive"},
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successo!")
            print(f"   Filtro applicato: {result.get('sentiment_filter', 'N/A')}")
            print(f"   Articoli filtrati: {result.get('total_filtered', 'N/A')}")
        elif response.status_code == 404:
            print("ℹ️ Nessuna news salvata trovata")
        else:
            print(f"❌ Errore: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completati!")

def test_app_status():
    """Testa lo stato generale dell'applicazione"""
    base_url = "http://localhost:5000"
    
    print("\n🔍 Test stato applicazione...")
    
    try:
        # Test homepage
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Homepage accessibile")
        else:
            print(f"❌ Errore homepage: {response.status_code}")
        
        # Test pagina news salvate
        response = requests.get(f"{base_url}/saved_news_page")
        if response.status_code == 200:
            print("✅ Pagina news salvate accessibile")
        else:
            print(f"❌ Errore pagina news salvate: {response.status_code}")
        
        # Test info utente
        response = requests.get(f"{base_url}/user_info")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Info utente: {result.get('user_id', 'N/A')}")
        else:
            print(f"❌ Errore info utente: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")

if __name__ == "__main__":
    print("🚀 Avvio test sentiment analysis...")
    
    # Test stato app
    test_app_status()
    
    # Test sentiment analysis
    test_sentiment_analysis()
    
    print("\n📝 Note:")
    print("- Assicurati che l'app sia in esecuzione su http://localhost:5000")
    print("- Il primo test potrebbe richiedere tempo per il download del modello FinBERT")
    print("- Se non ci sono news salvate, alcuni test mostreranno messaggi informativi") 