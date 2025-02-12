import asyncio
import aiohttp
from bs4 import BeautifulSoup
from utils import stopwatch
import aiohttp
import json
from newspaper import fulltext

@stopwatch(description='searching via searxng')
async def searxng(queries):

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_searxng(session, q) for q in queries]
        results = await gather(tasks)

    urls_data = {}
    for r in results:
        for k, v in r.items():
            if k not in urls_data:
                urls_data[k] = 0
            urls_data[k] += v
    urls_data = {
        k: v for k, v in sorted(
            urls_data.items(), 
            key=lambda item: item[1], reverse=True)
        }
    return list(urls_data.keys())[:15]

async def start_searching(decision_result: dict, query: str):

    urls = []

    queries = decision_result['queries']
    
    urls = await searxng(queries)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await gather(tasks)

    with open('to_parse.json', 'w', encoding='utf8') as f:
        json.dump(webpages, f, indent=2)

    results = [r for r in results if r]
    results = [r for r in results if r[1]]

    search_result = {
        "query": query,
        "retrieved_info": {r[0]:r[1] for r in results}
    }

    return search_result

@stopwatch(description='gathering')
async def gather(tasks):
    return await asyncio.gather(*tasks)

async def fetch_searxng(session, q):

    SEARXNG_URL = f"http://searxng:9998/search?format=json&q=google: {q}"

    urls_data = {}

    try:
        async with session.get(SEARXNG_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5) as response:
        
            if response.status == 200:
                results = await response.json()

                for n, r in enumerate(results['results']):

                    if r['parsed_url'][0] != 'https':
                        continue

                    url = r['url']
                    if not url in urls_data:
                        urls_data[url] = 0
                    urls_data[url] += len(results['results']) - n

            else:
                print(f"Ошибка: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")

    return urls_data

webpages = {}

# @stopwatch(description='gathering document')
async def fetch(session, url):
    try:
        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=1.25) as response:
            if response.status == 200:
                content = await response.text()
                webpages[url] = content
            else:
                return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    # Пробуем получить текст статьи
    article = None
    try:
        article = fulltext(content)
    except AttributeError as e:
        pass

    # Если не получили, пробуем спарсить текст через bs4
    if not article:
        selectors = [
            'article', 
            '.post-content', 
            '[itemprop="articleBody"]', 
            'div.content-wrapper'
            ]
    
        soup = BeautifulSoup(content, 'html.parser')
    
        for selector in selectors:
            article = soup.find(selector)
            if article:
                article = article.get_text('\n', True)
                break

    # В крайнем случае просто берём чистый текст веб-страницы
    if not article:
        soup = BeautifulSoup(content, 'html.parser')
        article = soup.get_text('\n', True)

    return (url, article if article else None)