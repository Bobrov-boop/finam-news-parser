import feedparser
import pandas as pd
from datetime import datetime
import requests
import os

def parse_finam_rss():
    """Парсинг новостей Finam через RSS"""
    rss_url = "https://www.finam.ru/analysis/conews/rsspoint/"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        content = None
        for encoding in ['utf-8', 'windows-1251', 'cp1251']:
            try:
                content = response.content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("❌ Не удалось декодировать")
            return []
        
        feed = feedparser.parse(content)
        
        news_list = []
        for entry in feed.entries[:50]:
            pub_date = entry.get('published', '') or entry.get('pubDate', '')
            date_str = ''
            if pub_date:
                try:
                    dt = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                    date_str = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = pub_date
            
            news_list.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'date': date_str,
                'description': entry.get('description', '')[:200],
                'source': 'finam_rss'
            })
        
        return news_list
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def main():
    print(f"🚀 Запуск: {datetime.now()}")
    
    news = parse_finam_rss()
    
    if not news:
        print("❌ Новостей нет")
        return
    
    df = pd.DataFrame(news)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Создаём папку
    os.makedirs('data', exist_ok=True)
    
    # Сохраняем файл
    filename = f'data/finam_{today}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ Сохранено {len(df)} новостей в {filename}")

if __name__ == "__main__":
    main()
