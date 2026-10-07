#!/usr/bin/env python3
"""usage: df_mark_img.py CODE [CODE...]  -> marks these codes as having a photo in dutyfree_all.json"""
import json,sys
fn='dutyfree_all.json';d=json.load(open(fn));d.setdefault('img',{})
for c in sys.argv[1:]:d['img'][c]=1
json.dump(d,open(fn,'w'),ensure_ascii=False,separators=(',',':'));print(len(d['img']),'photos marked')
