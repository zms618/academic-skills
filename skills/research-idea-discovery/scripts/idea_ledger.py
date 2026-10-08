#!/usr/bin/env python3
"""Local-only append-only Idea ledger with duplicate flags. Never uploads private ideas."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path


def signature(idea):
    text=' '.join(' '.join(str(idea.get(k,'')).casefold().split()) for k in ('domain','problem','hypothesis','mechanism'))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def add(path, idea):
    if not isinstance(idea,dict) or not all(idea.get(k) for k in ('idea_id','problem','hypothesis','mechanism','status')):
        raise ValueError('Ledger entry lacks idea_id, problem, hypothesis, mechanism, status')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    old=[]
    if path.exists():
        old=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    sig=signature(idea)
    duplicate=[x.get('idea_id') for x in old if x.get('signature')==sig]
    row={k:idea[k] for k in ('idea_id','problem','hypothesis','mechanism','status')}
    row['signature']=sig;row['duplicate_idea_ids']=duplicate
    row['updated_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    row['revisit_when']=idea.get('revisit_when','Only after material new evidence')
    with path.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return row

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--ledger',required=True);p.add_argument('--idea',required=True)
    a=p.parse_args(argv);print(json.dumps(add(a.ledger,json.loads(Path(a.idea).read_text(encoding='utf-8'))),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
