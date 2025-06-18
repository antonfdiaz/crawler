from src.crawl import fetch_crawl
import sys

visited = set()
results = {}

#ejecutar crawler
fetch_crawl(sys.argv[1],visited,results,0,2,50)

#guardar en json
import json
with open("results.json","w",encoding="utf-8") as f:
    json.dump(results,f,indent=4,ensure_ascii=False)