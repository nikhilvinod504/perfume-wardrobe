#!/usr/bin/env python3
"""prints done/remaining per shard (a code is done when it has an entry in enrich/out_NN.json, even m:0)"""
import json,glob,os
T=D=0
for q in sorted(glob.glob('enrich/q_*.tsv')):
    nn=q[-6:-4];codes=[l.split('\t')[0] for l in open(q,encoding='utf-8') if l.strip()]
    o='enrich/out_%s.json'%nn;d=json.load(open(o)) if os.path.exists(o) else {}
    done=sum(1 for c in codes if c in d);T+=len(codes);D+=done
    print(nn,done,'/',len(codes),'MISSING' if done<len(codes) else 'ok')
print('total',D,'/',T)
