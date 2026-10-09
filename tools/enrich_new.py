#!/usr/bin/env python3
"""Creates enrich/q_NN.tsv (code, brand, title) with every listed duty free code that has no enrichment entry yet
(an entry, even {"m":0}, in any enrich/out_*.json counts as done). Prints the shard number, or 'none' if nothing is new."""
import json,glob,re,os
d=json.load(open('dutyfree_all.json'));done=set()
for f in glob.glob('enrich/out_*.json'):done|=set(json.load(open(f)))
gone=set((d.get('gone') or {}).keys()) if isinstance(d.get('gone'),dict) else set()
new=[r for r in d['rows'] if r[0] not in done and r[0] not in gone and not (len(r)>8 and r[8])]
nums=[int(re.search(r'q_(\d+)',f).group(1)) for f in glob.glob('enrich/q_*.tsv')]
if not new:print('none');raise SystemExit
nn='%02d'%(max(nums)+1)
open('enrich/q_%s.tsv'%nn,'w',encoding='utf-8').write(''.join('%s\t%s\t%s\n'%(r[0],r[2],r[1]) for r in new))
print(nn,len(new))
