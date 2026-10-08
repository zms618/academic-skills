#!/usr/bin/env python3
"""Evidence-aware search coverage report; never claims exhaustive novelty."""
import argparse
import datetime as dt
import json
from pathlib import Path

AXES=('same_problem','same_mechanism','same_objective','cross_task_equivalent')

def report(record):
    if not isinstance(record,dict): record={}
    queries=record.get('queries',[])
    seen={a:[] for a in AXES}
    if isinstance(queries,list):
        for q in queries:
            if isinstance(q,dict) and q.get('axis') in seen and q.get('query') and q.get('source'):
                seen[q['axis']].append(q)
    coverage={a: 'RECORDED' if seen[a] else 'MISSING' for a in AXES}
    papers=record.get('paper_checks',[])
    checked=[p for p in papers if isinstance(p,dict) and p.get('evidence_level') in ('E2','E3')
             and p.get('url') and p.get('locator') and p.get('title')]
    latest = any(isinstance(q,dict) and q.get('search_date') for q in queries) if isinstance(queries,list) else False
    return {'status':'STRUCTURED_SEARCH_LOG_PRESENT' if all(seen.values()) and checked and latest else 'COVERAGE_INCOMPLETE',
            'query_axes':coverage,'fulltext_or_method_checked_count':len(checked),
            'search_dates_recorded':latest,'can_claim_novelty_exhaustive':False,
            'missing':[a for a in AXES if not seen[a]]+([] if checked else ['no verified fulltext/method citations'])
                      +([] if latest else ['missing search date']),
            'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'note':'Structured logs and declared E2/E3 locators are not proof a search was exhaustive or sources truthful.'}

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(argv)
    r=report(json.loads(Path(a.input).read_text(encoding='utf-8')))
    Path(a.out).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(r['status']);return 0 if r['status']=='STRUCTURED_SEARCH_LOG_PRESENT' else 2
if __name__=='__main__':raise SystemExit(main())
