#!/usr/bin/env python3
"""prints listed codes that have no photo yet (one per line), from dutyfree_all.json"""
import json
d=json.load(open('dutyfree_all.json'));img=d.get('img',{})
print('\n'.join(r[0]+'\t'+r[1] for r in d['rows'] if r[0] not in img))
