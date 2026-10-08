#!/usr/bin/env python3
"""Weekly merge for dutyfree_all.json.
usage: df_merge.py scraped.json [--date YYYY-MM-DD] [--force] [--file dutyfree_all.json]
scraped.json = {"A":[[code,title,mrp,price],...], "D":[[code,title,mrp,price],...]}  (arrivals / departure)
Rules: new codes -> rows + first[code]=date; price change -> chg[code]=[oldPrice,date];
missing codes -> gone (row + lastSeen at index 8); gone >28 days -> arch; back again -> restored.
Guard: if scrape has <90% of the previous listed count, abort unless --force (nothing is removed on a partial scrape)."""
import json,sys,os,datetime
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from dfclass import brand,gender
import re
a=sys.argv[1:]
date=a[a.index('--date')+1] if '--date' in a else datetime.date.today().isoformat()
fn=a[a.index('--file')+1] if '--file' in a else 'dutyfree_all.json'
force='--force' in a
S=json.load(open(a[0]));D=json.load(open(fn))
today=datetime.date.fromisoformat(date)
scr={}
for t,k in (('A','A'),('D','D')):
    for code,title,mrp,price in S.get(t,[]):
        e=scr.setdefault(code,{'t':title,'mrp':mrp,'p':price,'w':set()});e['w'].add(k)
old={r[0]:r for r in D['rows']}
if len(scr)<0.9*len(old) and not force:
    sys.exit('ABORT: scrape has %d items vs %d listed last time (<90%%). Nothing changed. Use --force only if the drop is real.'%(len(scr),len(old)))
first=D.get('first',{});chg=D.get('chg',{});gone={r[0]:r for r in D.get('gone',[])};arch={r[0]:r for r in D.get('arch',[])}
rows=[];stats={'new':0,'chg':0,'gone':0,'back':0,'arch':0}
for code,e in scr.items():
    term='AD' if len(e['w'])==2 else next(iter(e['w']))
    if code in old:
        r=list(old[code])
        if r[5]!=e['p']:chg[code]=[r[5],date];stats['chg']+=1
        r[4]=e['mrp'];r[5]=e['p'];r[6]=term
    elif code in gone or code in arch:
        r=list((gone.get(code) or arch.get(code))[:8]);r[4]=e['mrp'];r[5]=e['p'];r[6]=term
        gone.pop(code,None);arch.pop(code,None);stats['back']+=1
    else:
        t=e['t'].replace('Â','');r=[code,t,brand(t),gender(t),e['mrp'],e['p'],term,''];first[code]=date;stats['new']+=1
        if re.search(r"5th avenue|gucci rush|kylie|hair & body mist",t,re.I):r[3]='Women'
    rows.append(r)
for code,r in old.items():
    if code not in scr:gone[code]=list(r[:8])+[date];stats['gone']+=1
for code,r in list(gone.items()):
    if len(r)>8 and (today-datetime.date.fromisoformat(r[8])).days>28:
        arch[code]=r;del gone[code];stats['arch']+=1
# drop stale markers (older than 21 days)
cut=lambda d:(today-datetime.date.fromisoformat(d)).days>21
chg={k:v for k,v in chg.items() if not cut(v[1]) and k in scr}
# keep 'first' only for items still listed; NEW badge ages out in the app after 10 days
first={k:v for k,v in first.items() if k in scr and not cut(v)}
D['rows']=rows;D['gone']=list(gone.values());D['arch']=list(arch.values());D['first']=first;D['chg']=chg
D['asOf']=today.strftime('%-d %b %Y');D['asOfD']=date
# price history kept inside the file: hist={code:[[date,price],...]}; a point is added on first sight and whenever the price changes
H=D.get('hist',{})
for r in rows:
    h=H.setdefault(r[0],[])
    if not h or h[-1][1]!=r[5]:h.append([date,r[5]])
D['hist']=H
json.dump(D,open(fn,'w'),ensure_ascii=False,separators=(',',':'))
print(stats,'listed',len(rows),'gone',len(gone),'arch',len(arch))
