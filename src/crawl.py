import requests
from lxml import html
from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor,as_completed
import threading
import re

lock = threading.Lock()

def fetch_crawl(url,visited,results,depth,max_depth,word_limit):
    if depth > max_depth:
        return

    with lock:
        if url in visited:
            return
        visited.add(url)

    try:
        print(f"Crawling: {url}")
        res = requests.get(url,timeout=5)
        tree = html.fromstring(res.content)
        soup = BeautifulSoup(res.text,"html.parser")

        title = tree.findtext(".//title") or "Untitled"
        body = soup.find("body")

        if body:
            full_text = body.get_text(separator=" ")
            clean_text = re.sub(r"\s+"," ",full_text).strip()
            words = clean_text.split()
            content = " ".join(words[:word_limit])
        else:
            content = ""

        with lock:
            results.append({
                "url": url,
                "title": title,
                "content": content
            })

        links = tree.xpath("//a/@href")
        new_urls = []

        for link in links:
            full_url = urljoin(url, link)
            if full_url.startswith(("mailto:","tel:","javascript:","#")):
                continue
            parsed = urlparse(full_url)
            if parsed.scheme in ("http","https"):
                with lock:
                    if full_url not in visited:
                        new_urls.append(full_url)

        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for new_url in new_urls:
                futures.append(executor.submit(fetch_crawl,new_url,visited,results,depth+1,max_depth,word_limit))
            for future in as_completed(futures):
                pass

    except Exception as e:
        print(f"Error with {url}: {e}")