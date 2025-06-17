from src.crawl import crawl
import json

#ejecutar el crawler
results = crawl("http://example.com")

#guardar en un json bonito :)
with open("urls.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)