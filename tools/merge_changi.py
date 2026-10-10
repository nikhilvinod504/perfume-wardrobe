#!/usr/bin/env python3
"""run after enrich_merge.py: copy Fragrantica entries to duplicate Changi/D&S codes (same perfume) and to cross-shop family members"""
import json,copy
p=json.load(open('enrich/plan_changi.json'));d=json.load(open('dutyfree_info.json'));it=d['items']
n=0
for code,src in p['inherit'].items():
    if code not in it and src in it: it[code]=copy.deepcopy(it[src]);n+=1
for lead,codes in p['groups'].items():
    if lead in it:
        for c in codes:
            if c not in it: it[c]=copy.deepcopy(it[lead]);n+=1
json.dump(d,open('dutyfree_info.json','w'),ensure_ascii=False,separators=(',',':'))
print('inherited',n,'total',len(it))
