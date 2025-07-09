#!/usr/bin/env python3
"""
Test script per i provider di news italiane
"""

import requests
import json
import time

def test_italian_providers():
    """Testa i provider italiani disponibili"""
    
    base_url = "http://localhost:5000"
    
    # Test 1: Verifica provider disponibili
    print("🔍 Test 1: Verifica provider disponibili")
    try:
        response = requests.get(f"{base_url}/italian_providers")
        providers = response.json()
        print(f"✅ Provider disponibili: {providers}")
    except Exception as e:
        print(f"❌ Errore nel test provider: {e}")
        return
    
    # Test 2: Ricerca news per ticker italiano (ENEL)
    print("\n🔍 Test 2: Ricerca news per ENEL su ANSA")
    try:
        response = requests.post(f"{base_url}/search_ticker_news", 
                               json={
                                   "tickers": ["ENEL"],
                                   "days_back": 7,
                                   "provider": "ansa"
                               })
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Trovate {data['total_articles']} news da ANSA")
            for i, article in enumerate(data['articles'][:3]):  # Mostra primi 3
                print(f"  {i+1}. {article['title'][:80]}...")
                print(f"     Fonte: {article['source']}")
                print(f"     Data: {article['publishedAt']}")
        else:
            print(f"❌ Errore: {data.get('error', 'Errore sconosciuto')}")
    except Exception as e:
        print(f"❌ Errore nel test ANSA: {e}")
    
    # Test 3: Ricerca news per ticker su Il Sole 24 Ore
    print("\n🔍 Test 3: Ricerca news per ENI su Il Sole 24 Ore")
    try:
        response = requests.post(f"{base_url}/search_ticker_news", 
                               json={
                                   "tickers": ["ENI"],
                                   "days_back": 7,
                                   "provider": "ilsole24ore"
                               })
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Trovate {data['total_articles']} news da Il Sole 24 Ore")
            for i, article in enumerate(data['articles'][:3]):  # Mostra primi 3
                print(f"  {i+1}. {article['title'][:80]}...")
                print(f"     Fonte: {article['source']}")
                print(f"     Data: {article['publishedAt']}")
        else:
            print(f"❌ Errore: {data.get('error', 'Errore sconosciuto')}")
    except Exception as e:
        print(f"❌ Errore nel test Il Sole 24 Ore: {e}")
    
    # Test 4: Ricerca news per ticker su La Repubblica
    print("\n🔍 Test 4: Ricerca news per TIM su La Repubblica")
    try:
        response = requests.post(f"{base_url}/search_ticker_news", 
                               json={
                                   "tickers": ["TIM"],
                                   "days_back": 7,
                                   "provider": "repubblica"
                               })
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Trovate {data['total_articles']} news da La Repubblica")
            for i, article in enumerate(data['articles'][:3]):  # Mostra primi 3
                print(f"  {i+1}. {article['title'][:80]}...")
                print(f"     Fonte: {article['source']}")
                print(f"     Data: {article['publishedAt']}")
        else:
            print(f"❌ Errore: {data.get('error', 'Errore sconosciuto')}")
    except Exception as e:
        print(f"❌ Errore nel test La Repubblica: {e}")
    
    # Test 5: Ricerca news per ticker su Corriere della Sera
    print("\n🔍 Test 5: Ricerca news per UniCredit su Corriere della Sera")
    try:
        response = requests.post(f"{base_url}/search_ticker_news", 
                               json={
                                   "tickers": ["UCG"],
                                   "days_back": 7,
                                   "provider": "corriere"
                               })
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Trovate {data['total_articles']} news da Corriere della Sera")
            for i, article in enumerate(data['articles'][:3]):  # Mostra primi 3
                print(f"  {i+1}. {article['title'][:80]}...")
                print(f"     Fonte: {article['source']}")
                print(f"     Data: {article['publishedAt']}")
        else:
            print(f"❌ Errore: {data.get('error', 'Errore sconosciuto')}")
    except Exception as e:
        print(f"❌ Errore nel test Corriere: {e}")
    
    # Test 6: Ricerca news per ticker su Bloomberg
    print("\n🔍 Test 6: Ricerca news per Ferrari su Bloomberg")
    try:
        response = requests.post(f"{base_url}/search_ticker_news", 
                               json={
                                   "tickers": ["RACE"],
                                   "days_back": 7,
                                   "provider": "bloomberg_italia"
                               })
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Trovate {data['total_articles']} news da Bloomberg")
            for i, article in enumerate(data['articles'][:3]):  # Mostra primi 3
                print(f"  {i+1}. {article['title'][:80]}...")
                print(f"     Fonte: {article['source']}")
                print(f"     Data: {article['publishedAt']}")
        else:
            print(f"❌ Errore: {data.get('error', 'Errore sconosciuto')}")
    except Exception as e:
        print(f"❌ Errore nel test Bloomberg: {e}")

if __name__ == "__main__":
    print("🚀 Test Provider News Italiane")
    print("=" * 50)
    
    # Verifica che il server sia in esecuzione
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Server Flask in esecuzione")
            test_italian_providers()
        else:
            print("❌ Server non risponde correttamente")
    except requests.exceptions.ConnectionError:
        print("❌ Impossibile connettersi al server Flask")
        print("   Assicurati che il server sia in esecuzione con: python app.py")
    except Exception as e:
        print(f"❌ Errore di connessione: {e}") 