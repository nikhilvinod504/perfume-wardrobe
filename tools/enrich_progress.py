#!/usr/bin/env python3
"""writes enrich/progress.json {done,total,matched,at}"""
import json,glob,datetime
tot=sum(1 for q in glob.glob('enrich/q_*.tsv') for l in open(q,encoding='utf-8') if l.strip())
d=m=0
for f in glob.glob('enrich/out_*.json'):
    for v in json.load(open(f)).values():d+=1;m+=1 if v.get('m') else 0
json.dump({"done":d,"total":tot,"matched":m,"at":datetime.datetime.utcnow().isoformat()+"Z"},open('enrich/progress.json','w'))
print(d,'/',tot,'matched',m)
