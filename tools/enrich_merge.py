#!/usr/bin/env python3
"""merge enrich/out_*.json -> dutyfree_info.json (matched entries only)"""
import json,glob,datetime
items={}
for f in sorted(glob.glob('enrich/out_*.json')):
    for k,v in json.load(open(f)).items():
        if v.get('m') and (v.get('a') or v.get('t') or v.get('h') or v.get('b')):items[k]=v
json.dump({"asOf":datetime.date.today().strftime('%-d %b %Y'),"source":"Fragrantica via Apify","items":items},open('dutyfree_info.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(items),'perfumes in dutyfree_info.json')
