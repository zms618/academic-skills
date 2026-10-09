#!/usr/bin/env python3
"""Structural problem/motivation evidence screen; never verifies a published claim.

Outputs a non-promotional status. No method-related field may be treated as
motivation evidence. PASS_FOR_IDEATION is *structural*, not scientific approval.
"""
import argparse
import json
from pathlib import Path

DIRECT = {'DIRECT_TABLE','DIRECT_REPLICATION','DIRECT_THEOREM','BENCHMARK_ANALYSIS'}
WEAK = {'ABSTRACT_ONLY','CLAIM_ONLY','HYPOTHESIZED'}

def filled(x):
    return isinstance(x,str) and len(x.strip()) >= 12 and x.strip().lower() not in {
        'tbd','unknown','novel idea','improve performance','improve robustness',
        '提高鲁棒性','提升性能','新的研究问题','待验证','暂无数据'}

def assess(card):
    if not isinstance(card,dict): card={}
    issues=[]
    required=['problem_id','task_context','scientific_question','concrete_observation',
              'observable_measure','baseline_reference','problem_importance','falsification_probe',
              'bounded_probe','independence_scope']
    for k in required:
        if not filled(card.get(k)):
            issues.append('missing_or_weak_'+k)
    alts=card.get('alternative_explanations',[])
    if not isinstance(alts,list) or len([x for x in alts if filled(x)])<2:
        issues.append('need_two_competing_explanations')
    conf=card.get('confounder_checks',[])
    if not isinstance(conf,list) or len([x for x in conf if filled(x)])<2:
        issues.append('need_two_confounder_controls')
    ev=card.get('evidence',[])
    if not isinstance(ev,list):ev=[]
    direct=[]
    for i,e in enumerate(ev):
        if not isinstance(e,dict):issues.append('invalid_evidence_entry_'+str(i));continue
        kind=e.get('evidence_type','')
        if kind in DIRECT:
            if all(filled(e.get(k)) for k in ('source','locator','what_observed','independence_key')):
                direct.append(e)
            else:issues.append('missing_primary_source_or_locator_'+str(i))
        elif kind not in WEAK:
            issues.append('unknown_evidence_type_'+str(i))
    units={e['independence_key'].strip().lower() for e in direct}
    # Different claims inside one paper don't become independent by relabeling.
    special=(len(direct)==1 and direct[0].get('evidence_type') in {'DIRECT_THEOREM','DIRECT_REPLICATION'} and
             direct[0].get('independently_reproducible') is True)
    has_core=not issues
    contradicted=card.get('contradicted_by_control') is True or card.get('failure_disappears_under_fair_comparison') is True
    if contradicted:
        status='REJECT_OR_REFRAME'
        issues.append('problem_premise_negated_by_control')
    elif has_core and (len(units)>=2 or special):
        status='PASS_FOR_IDEATION'
    elif direct:
        status='PROBE_ONLY'
        issues.append('insufficient_independent_support_or_controls')
    elif card.get('source_access_blocked') is True:
        status='RESEARCH_MORE'
        issues.append('source_access_unverified')
    else:
        status='REJECT_OR_REFRAME'
        issues.append('no_located_direct_problem_evidence')
    return {'status':status,'ready':status=='PASS_FOR_IDEATION',
       'can_generate_idea_seeds':status=='PASS_FOR_IDEATION',
       'direct_evidence_units':len(units), 'issues':sorted(set(issues)),
       'allowed_next_action': 'IDEA_SEED' if status=='PASS_FOR_IDEATION' else
         ('NO_NEW_MODEL_PROBLEM_PROBE' if status=='PROBE_ONLY' else
          ('NEUTRAL_EVIDENCE_SEARCH' if status=='RESEARCH_MORE' else 'NEW_PROBLEM_SCOUT')),
       'limitations':'Structural source/field check only: URLs, experimental fairness, importance and independence NOT independently verified.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args()
    r=assess(json.loads(Path(a.input).read_text(encoding='utf-8')))
    if a.output:Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['ready'] else 2
if __name__=='__main__':raise SystemExit(main())
