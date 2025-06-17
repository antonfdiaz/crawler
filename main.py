from src.crawl import crawl
import json
import sys

#ejecutar el crawler
results = crawl(sys.argv[1])

#guardar en un json bonito :)
with open("urls.json","w",encoding="utf-8") as f:
    json.dump(results,f,indent=4,ensure_ascii=False)