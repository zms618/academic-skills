#!/usr/bin/env python3
"""Dataset metadata lead discovery; NOT an access, license or suitability verifier.

Public APIs: Hugging Face Hub datasets listing; Zenodo records search.
Do not submit confidential unpublished ideas to external search systems.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER_AGENT='ResearchIdeaDiscovery/2.4 (public metadata research; no automated downloads)'


def normalize_hf(payload):
    if not isinstance(payload,list):return []
    out=[]
    for item in payload:
        if not isinstance(item,dict):continue
        ident=item.get('id')
        if not isinstance(ident,str) or not ident.strip():continue
        out.append({'platform':'Hugging Face', 'dataset_id':ident,
                    'title':ident, 'url':'https://huggingface.co/datasets/'+ident,
                    'last_modified':item.get('lastModified'),
                    'tags':item.get('tags',[]) if isinstance(item.get('tags'),list) else [],
                    'evidence':'CATALOG_METADATA_ONLY', 'access_confirmed':False,
                    'license_confirmed':False, 'task_fit_confirmed':False})
    return out


def normalize_zenodo(payload):
    rows=payload.get('hits',{}).get('hits',[]) if isinstance(payload,dict) else []
    out=[]
    for item in rows:
        if not isinstance(item,dict):continue
        meta=item.get('metadata') or {}; links=item.get('links') or {}
        title=meta.get('title')
        url=links.get('html') or (f"https://zenodo.org/records/{item['id']}" if item.get('id') else None)
        if not title or not url:continue
        out.append({'platform':'Zenodo','dataset_id':str(item.get('id','')),
                    'title':title,'url':url,'date':meta.get('publication_date'),
                    'resource_type':meta.get('resource_type'),
                    'evidence':'CATALOG_METADATA_ONLY', 'access_confirmed':False,
                    'license_confirmed':False,'task_fit_confirmed':False})
    return out


def _get_json(url,timeout=12):
    req=Request(url,headers={'User-Agent':USER_AGENT,'Accept':'application/json'})
    with urlopen(req,timeout=timeout) as response:
        return json.load(response)


def discover(query,limit=12,fixture_dir=None):
    if not isinstance(query,str) or not query.strip():raise ValueError('Nonempty topic required')
    if not isinstance(limit,int) or not 1<=limit<=100:raise ValueError('limit between 1 and 100')
    fixture=Path(fixture_dir) if fixture_dir is not None else None
    sources=[
        ('huggingface','https://huggingface.co/api/datasets?'+urlencode({'search':query,'limit':limit}),normalize_hf),
        ('zenodo','https://zenodo.org/api/records/?'+urlencode({'q':query,'size':limit}),normalize_zenodo)]
    hits=[];logs=[]
    for key,url,parser in sources:
        try:
            if fixture:
                payload=json.loads((fixture/(key+'.json')).read_text(encoding='utf-8'))
            else:
                payload=_get_json(url)
            parsed=parser(payload)
            hits.extend(parsed)
            logs.append({'source':key,'count':len(parsed),'status':'FIXTURE' if fixture else 'METADATA_FETCH_OK'})
        except Exception as e:
            logs.append({'source':key,'count':0,'status':'ERROR','message':str(e)[:250]})
    dedup=[];seen=set()
    for hit in hits:
        sig=(hit['platform'],hit['dataset_id'])
        if sig not in seen:
            dedup.append(hit);seen.add(sig)
    return {'query':query,'as_of_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'status':'FIXTURE_ONLY' if fixture else ('CATALOG_SEARCH_DONE' if any(x['status']=='METADATA_FETCH_OK' for x in logs) else 'UNAVAILABLE'),
            'logs':logs,'leads':dedup,
            'next_actions':['For each plausible lead, inspect dataset documentation and actual fields',
                            'Inspect license and any access restrictions',
                            'Verify train/test protocol, label availability, baseline and budget',
                            'Build dataset_anchor card only after actual source evidence is obtained'],
            'disclaimer':'Dataset catalog hits are search leads only; no files downloaded, no license/access/task-fit verified.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--query',required=True);p.add_argument('--limit',type=int,default=12)
    p.add_argument('--fixture-dir');p.add_argument('--out',required=True)
    a=p.parse_args();result=discover(a.query,a.limit,a.fixture_dir)
    output=Path(a.out);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'],len(result['leads']),'metadata leads ->',str(output))
    return 0 if result['leads'] else 2

if __name__=='__main__':raise SystemExit(main())
