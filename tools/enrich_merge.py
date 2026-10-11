#!/usr/bin/env python3
"""merge enrich/out_*.json -> dutyfree_info.json, stored ONCE per Fragrantica perfume.
Format: {"asOf","source","p":{fragranticaId: entry}, "c":{code: fragranticaId}}.
Codes without their own lookup reuse the entry of the same perfume: Changi/D&S plan (enrich/plan_changi.json),
cross-shop families (xshop.json) and sizes of one Bali perfume (BL<sku>_<ml>)."""
import json,glob,datetime,re,os
own={}
for f in sorted(glob.glob('enrich/out_*.json')):
    for k,v in json.load(open(f)).items():
        if v.get('m') and (v.get('a') or v.get('t') or v.get('h') or v.get('b')):
            for kk in ('t','h','b','o'):
                if isinstance(v.get(kk),str):v[kk]=[a.strip() for a in v[kk].split(',') if a.strip()]
            own[k]=v
P={};C={}
def fid(v):return str(v.get('id') or v.get('u') or v.get('n'))
for k,v in own.items():
    i=fid(v);P.setdefault(i,v);C[k]=i
n0=len(C)
def share(src,dst):
    if dst not in C and src in C:C[dst]=C[src];return 1
    return 0
if os.path.exists('enrich/plan_changi.json'):
    p=json.load(open('enrich/plan_changi.json'))
    for code,src in p['inherit'].items():share(src,code)
    for lead,codes in p['groups'].items():
        for c in codes:share(lead,c)
if os.path.exists('xshop.json'):
    x=json.load(open('xshop.json'))
    for F in x['f']:
        d=next((o[1] for o in F if o[1] in C),None)
        if d:
            for o in F:share(d,o[1])
if os.path.exists('bali_all.json'):
    par=lambda c:re.sub(r'_\d+$','',c)
    lead={}
    for c in C:
        if c.startswith('BL'):lead.setdefault(par(c),c)
    for r in json.load(open('bali_all.json'))['rows']:
        if r[0].startswith('BL') and par(r[0]) in lead:share(lead[par(r[0])],r[0])
json.dump({"asOf":datetime.date.today().strftime('%-d %b %Y'),"source":"Fragrantica via Apify","p":P,"c":C},open('dutyfree_info.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(P),'perfumes stored once;',len(C),'codes (',n0,'own lookups )')
