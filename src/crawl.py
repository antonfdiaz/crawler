import requests
from lxml import html
from urllib.parse import urljoin, urlparse
import json

def crawl(url, visited=None, results=None, depth=0, max_depth=2):
    if visited is None:
        visited = set()
    if results is None:
        results = {}

    if depth > max_depth or url in visited:
        return

    try:
        print(f"Crawling: {url}")
        visited.add(url)

        response = requests.get(url, timeout=5)
        tree = html.fromstring(response.content)

        title = tree.findtext('.//title') or "Sin título"

        #guardar en memoria
        results[url] = {
            "title": title
        }

        #extraer enlaces
        links = tree.xpath("//a/@href")

        for link in links:
            full_url = urljoin(url,link)

            #ignorar enlaces malvados >:(
            if full_url.startswith(("mailto:","tel:","javascript:","#")):
                continue

            parsed = urlparse(full_url)

            if parsed.scheme in ("http","https") and full_url not in visited:
                crawl(full_url,visited,results,depth+1,max_depth)

    except Exception as e:
        print(f"Error con {url}: {e}")

    return results