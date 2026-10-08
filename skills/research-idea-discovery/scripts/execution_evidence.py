#!/usr/bin/env python3
"""Check local review and pilot *artifacts*, not scientific truth.

Never equate a plan, self-scored form, or dry run with a performed experiment.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def review_record(card):
    if not isinstance(card, dict):
        return {'ready': False, 'status': 'REVIEW_MISSING', 'issues': ['review record required']}
    issues=[]
    if not card.get('idea_id') or not isinstance(card.get('revision'), int):
        issues.append('idea_id and integer revision required')
    if card.get('verdict') != 'PROCEED_TO_PILOT':
        issues.append('review verdict must explicitly authorize moving to pilot; STOP/REVISE cannot pass')
    objections=card.get('objections', [])
    if not isinstance(objections, list) or len(objections)<2 or any(not isinstance(x,dict) or not x.get('concern') or not x.get('evidence_or_response') for x in objections):
        issues.append('at least 2 documented reviewer objections and evidence/response required')
    if card.get('critical_objections_unresolved') is not False:
        issues.append('critical reviewer objections unresolved or unchecked')
    return {'ready':not issues,'status':'REVIEW_RECORD_READY_NOT_INDEPENDENT_VERIFICATION' if not issues else 'REVIEW_UNRESOLVED',
            'idea_id':card.get('idea_id'),'revision':card.get('revision'),'issues':issues,
            'disclaimer':'Record/decision audit. Simulated roles are not independent model reviewers.'}


def pilot_record(run_dir, metrics_path=None):
    root=Path(run_dir)
    logpath=root/'pilot_run.json'
    if not logpath.is_file():
        return {'ready': False, 'status':'NO_RUN_LOG', 'issues':['pilot_run.json missing']}
    try:
        log=json.loads(logpath.read_text(encoding='utf-8'))
    except (ValueError,OSError):
        return {'ready':False,'status':'INVALID_RUN_LOG','issues':['Cannot read run log']}
    issues=[]
    status=log.get('status')
    if not log.get('authorized_execute') or status not in ('RUN_COMPLETE','RUN_FAILED'):
        issues.append('DRY_RUN/TIMEOUT/EXEC_ERROR is not completed pilot evidence')
    if status == 'RUN_FAILED':
        stderr=root/'stderr.txt'
        if not stderr.is_file():issues.append('failed pilot must preserve error log')
        return {'ready':not issues,'status':'FAILED_RUN_DOCUMENTED' if not issues else 'FAILED_UNDOCUMENTED',
                'requires_reaudit': True, 'issues':issues, 'run_status':status,
                'disclaimer':'Failure is useful evidence but not experimental success.'}
    if log.get('returncode')!=0:
        issues.append('successful run needs returncode 0')
    stdout=root/'stdout.txt'
    if not stdout.is_file() or hashlib.sha256(stdout.read_bytes()).hexdigest()!=log.get('stdout_sha256'):
        issues.append('run stdout absent or checksum mismatch')
    if not metrics_path:
        issues.append('metric file required; successfully executing code is not a scientific result')
        metrics={}
    else:
        path=Path(metrics_path)
        try:
            metrics=json.loads(path.read_text(encoding='utf-8'))
        except (OSError,ValueError):
            metrics={};issues.append('invalid metrics JSON')
    for key in ('metric_name','direction','baseline','proposed','dataset_split','idea_id','revision'):
        if key not in metrics or metrics[key] in ('',None):issues.append('metrics missing '+key)
    if metrics.get('direction') not in ('higher','lower'):issues.append('metric direction must be higher or lower')
    for key in ('baseline','proposed'):
        v=metrics.get(key)
        if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v):issues.append('numeric finite '+key+' required')
    if status!='RUN_COMPLETE':issues.append('no successful run')
    rival_better_or_equal=False
    if not issues:
        rival_better_or_equal=(metrics['proposed'] <= metrics['baseline'] if metrics['direction']=='higher'
                               else metrics['proposed'] >= metrics['baseline'])
    return {'ready':not issues,'status':'MEASUREMENTS_RECORDED' if not issues else 'PILOT_EVIDENCE_INCOMPLETE',
            'requires_reaudit':rival_better_or_equal,
            'mechanism_necessity':'NOT_ESTABLISHED_BY_THIS_PILOT' if rival_better_or_equal else 'NOT_PROVEN_BY_ONE_PILOT',
            'issues':issues,'run_status':status, 'metrics':metrics if not issues else {},
            'limitations':'Metrics supplied by an actual local artifact, but statistical validity, benchmark legitimacy and absence of leakage require external checks.'}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('review');a.add_argument('--card',required=True);a.add_argument('--out',required=True)
    b=sub.add_parser('pilot');b.add_argument('--run-dir',required=True);b.add_argument('--metrics');b.add_argument('--out',required=True)
    a=ap.parse_args(argv)
    r=review_record(json.loads(Path(a.card).read_text(encoding='utf-8'))) if a.cmd=='review' else pilot_record(a.run_dir,a.metrics)
    Path(a.out).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(r['status']);return 0 if r['ready'] else 2

if __name__=='__main__':raise SystemExit(main())
