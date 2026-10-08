#!/usr/bin/env python3
"""OpenAlex + Crossref bibliographic discovery. Metadata is not proof of novelty.

Standard-library implementation, written for this plugin (not copied upstream).
Examples:
  python scripts/literature_search.py --query 'test time adaptation' --out result.json
  python scripts/literature_search.py --query 'test time adaptation' --fixture-dir tests/fixtures --out result.json
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT='ResearchIdeaDiscovery/2.0 (academic metadata research; contact supplied by user)'

def norm_title(s):
    return re.sub(r'[^a-z0-9]+','',s.casefold())

def norm_doi(s):
    if not s: return ''
    s=str(s).strip().lower()
    return re.sub(r'^https?://(dx\.)?doi\.org/','',s)

def parse_openalex(data):
    result=[]
    for x in data.get('results',[]):
        if not x.get('title'):continue
        loc=x.get('primary_location') or {}
        rec={'title':x['title'],'doi':norm_doi(x.get('doi')),'year':x.get('publication_year'),
             'url':x.get('doi') or x.get('id') or (loc.get('landing_page_url')),
             'source':['openalex'],'source_id':[str(x.get('id',''))],
             'cited_by_count':x.get('cited_by_count'), 'fulltext_verified':False,
             'claim_checked':False,'evidence_level':'METADATA_ONLY'}
        result.append(rec)
    return result

def parse_crossref(data):
    result=[]
    for x in (data.get('message') or {}).get('items',[]):
        title=(x.get('title') or [''])[0]
        if not title:continue
        dates=x.get('published') or x.get('created') or {}
        parts=dates.get('date-parts') or [[]]
        year=parts[0][0] if parts and parts[0] else None
        doi=norm_doi(x.get('DOI'))
        rec={'title':title,'doi':doi,'year':year,
             'url':x.get('URL') or ('https://doi.org/'+doi if doi else ''),
             'source':['crossref'],'source_id':[str(x.get('DOI',''))],
             'cited_by_count':x.get('is-referenced-by-count'), 'fulltext_verified':False,
             'claim_checked':False,'evidence_level':'METADATA_ONLY'}
        result.append(rec)
    return result

def merge(records):
    # deterministic stable dedup DOI first, normalized title second
    items=[];doi_index={};title_index={}
    for x in records:
        doi=x['doi']; title=norm_title(x['title']); i=doi_index.get(doi) if doi else None
        if i is None: i=title_index.get(title)
        if i is None:
            x=dict(x); items.append(x);i=len(items)-1
        else:
            old=items[i]
            old['source']=sorted(set(old['source']+x['source']))
            old['source_id']=sorted(set(old['source_id']+x['source_id']))
            if not old['doi'] and doi:old['doi']=doi
            if not old['url'] and x['url']:old['url']=x['url']
            if old['year'] is None and x['year'] is not None:old['year']=x['year']
        if doi:doi_index[doi]=i
        if title:title_index[title]=i
    return items

def fetch_json(base,params,timeout=12):
    url=base+'?'+urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':USER_AGENT}),timeout=timeout) as h:
        raw=h.read(12_000_000)
    return json.loads(raw.decode('utf-8')),url

def run(query,limit=12,fixture_dir=None,email=None,offline=False):
    if not query.strip():raise ValueError('Search query required')
    if not 1 <= limit <= 100:raise ValueError('limit must be 1..100')
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    result={'query':query,'searched_at_utc':now,'notice':'Bibliographic metadata only; no full text or novelty verification',
            'providers':{},'records':[],'status':'INCOMPLETE'}
    providers=[('openalex','https://api.openalex.org/works',{'search':query,'per_page':limit},parse_openalex),
               ('crossref','https://api.crossref.org/works',{'query.bibliographic':query,'rows':limit},parse_crossref)]
    data=[]
    for name,base,params,parser in providers:
        if name=='openalex' and os.environ.get('OPENALEX_API_KEY'):
            params['api_key']=os.environ['OPENALEX_API_KEY']
        if name=='crossref' and email:
            params['mailto']=email
        url=base+'?'+urllib.parse.urlencode({k:v for k,v in params.items() if k!='api_key'})
        try:
            if fixture_dir:
                item=json.loads((Path(fixture_dir)/(name+'.json')).read_text(encoding='utf8'))
                status='FIXTURE_ONLY'
            elif offline:raise RuntimeError('offline selected and no fixture supplied')
            else:
                item,_=fetch_json(base,params);status='OK'
                time.sleep(0.2)
            rs=parser(item);data.extend(rs)
            result['providers'][name]={'status':status,'count':len(rs),'query_url_without_key':url}
        except (OSError,ValueError,KeyError,RuntimeError,urllib.error.URLError) as e:
            result['providers'][name]={'status':'ERROR','message':str(e)[:300], 'query_url_without_key':url}
    result['records']=merge(data)
    statuses=[a['status'] for a in result['providers'].values()]
    result['status']=('FIXTURE_ONLY' if all(s=='FIXTURE_ONLY' for s in statuses) else
                      'OK' if all(s=='OK' for s in statuses) else
                      'PARTIAL' if any(s in ('OK','FIXTURE_ONLY') for s in statuses) else 'ERROR')
    return result

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--query',required=True);ap.add_argument('--limit',type=int,default=12)
    ap.add_argument('--out',required=True);ap.add_argument('--fixture-dir');ap.add_argument('--offline',action='store_true')
    ap.add_argument('--email',help='Your email for Crossref polite pool (not stored in result)')
    args=ap.parse_args(argv)
    report=run(args.query,args.limit,args.fixture_dir,args.email,args.offline)
    p=Path(args.out);p.parent.mkdir(exist_ok=True,parents=True)
    if p.suffix.lower()=='.csv':
        with p.open('w',encoding='utf-8',newline='') as f:
            keys=['title','doi','year','url','source','evidence_level','fulltext_verified']
            w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
            for r in report['records']:
                w.writerow({k:';'.join(v) if isinstance(v,list) else v for k,v in r.items() if k in keys})
        p.with_suffix('.metadata.json').write_text(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2,ensure_ascii=False),encoding='utf-8')
    else:p.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f"{report['status']}: {len(report['records'])} deduplicated metadata records -> {p}")
    return 1 if report['status']=='ERROR' else 0
if __name__=='__main__':sys.exit(main())
