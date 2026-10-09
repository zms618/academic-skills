#!/usr/bin/env python3
"""Check PAPER-ANCHORED research lineage structural claims only, never academic truth."""
import argparse
import json
from pathlib import Path

ROLES={'ANCHOR','BENCHMARK','RIVAL','MECHANISM','CONTRADICTION','CROSS_DOMAIN'}
READ={'ABSTRACT_LEAD','MAIN_PAPER_READ','TABLE_LOCATED','APPENDIX_READ','CODE_INSPECTED','REPLICATION_LOG'}
EVIDENCED=READ-{'ABSTRACT_LEAD'}
ASSET={'DISCOVERED_LINK','LICENSE_CHECKED','CONFIG_INSPECTED','WEIGHTS_LOCATED','WEIGHTS_LOADED','MINI_INFERENCE_EXECUTED','BASELINE_REPRODUCED','BLOCKED','UNKNOWN'}

def detail(value):
    return isinstance(value,str) and len(value.strip())>=12 and value.strip().lower() not in {'unknown','not checked','tbd','n/a'}

def assess(card):
    if not isinstance(card,dict):card={}
    issues=[];papers=card.get('papers',[])
    if not isinstance(papers,list):papers=[]
    if not 3<=len(papers)<=8:issues.append('need_three_to_eight_adversarial_anchor_papers_or_choose_open_problem_mode')
    ids=[];roles=[];located=0
    for i,p in enumerate(papers):
        if not isinstance(p,dict):issues.append(f'paper_{i}_not_object');continue
        pid=p.get('paper_id');ids.append(pid);roles.append(p.get('role'))
        for field in ('paper_id','title','source_url','task_protocol','reported_observation','counterpoint'):
            if not ((isinstance(p.get(field),str) and bool(p[field].strip())) if field=='paper_id' else detail(p.get(field))):
                issues.append(f'paper_{i}_missing_{field}')
        if not str(p.get('source_url','')).startswith(('https://','http://')):
            issues.append(f'paper_{i}_source_url_not_http')
        if p.get('role') not in ROLES:issues.append(f'paper_{i}_unknown_role')
        if p.get('reading_depth') not in READ:issues.append(f'paper_{i}_invalid_reading_depth')
        if p.get('reading_depth') in EVIDENCED and detail(p.get('evidence_locator')):
            located+=1
        elif p.get('reading_depth') in EVIDENCED:
            issues.append(f'paper_{i}_no_located_evidence_for_reading_claim')
        for field in ('code_status','dataset_status','checkpoint_status'):
            if p.get(field) not in ASSET:issues.append(f'paper_{i}_invalid_{field}')
        if p.get('code_status') in {'MINI_INFERENCE_EXECUTED','BASELINE_REPRODUCED'} or p.get('checkpoint_status') in {'WEIGHTS_LOADED','MINI_INFERENCE_EXECUTED','BASELINE_REPRODUCED'}:
            if not detail(p.get('execution_log')): issues.append(f'paper_{i}_execution_claim_without_log')
    if len(set(ids))!=len(ids):issues.append('duplicate_paper_id')
    if len(set(roles))<2:issues.append('need_distinct_paper_roles_not_just_favorite_work')
    if not {'RIVAL','CONTRADICTION','BENCHMARK'}.intersection(roles):issues.append('no_adversarial_or_negative_result_paper')
    if located<2:issues.append('need_two_located_paper_evidence_units_no_abstract_only_portfolio')
    problems=card.get('problem_lineage',[])
    if not isinstance(problems,list) or not problems:issues.append('no_paper_to_problem_lineage');problems=[]
    for i,m in enumerate(problems):
        if not isinstance(m,dict):issues.append(f'problem_{i}_not_object');continue
        source_ids=m.get('source_paper_ids',[])
        if not isinstance(source_ids,list) or not source_ids or any(x not in ids for x in source_ids):
            issues.append(f'problem_{i}_has_no_real_paper_reference')
        for field in ('problem_id','observed_vs_hypothesized','null_explanation','minimal_falsifier'):
            if not ((isinstance(m.get(field),str) and bool(m[field].strip())) if field=='problem_id' else detail(m.get(field))):
                issues.append(f'problem_{i}_missing_{field}')
        if m.get('status') not in {'HYPOTHESIS','PROBE_ONLY','M0_READY_TO_CHECK','REJECTED'}:
            issues.append(f'problem_{i}_invalid_evidence_status')
        if any(x in m for x in ('proposed_method','architecture','three_contributions','method_name')):
            issues.append(f'problem_{i}_premature_solution_first')
    for i,conf in enumerate(card.get('contradictions',[]) or []):
        if not isinstance(conf,dict): issues.append(f'contradiction_{i}_invalid');continue
        pair=conf.get('paper_ids',[])
        if not isinstance(pair,list) or len(pair)!=2 or len(set(pair))!=2 or any(x not in ids for x in pair):
            issues.append(f'contradiction_{i}_paper_pair_invalid')
        if conf.get('status')=='ESTABLISHED' and not detail(conf.get('matched_protocol_evidence')):
            issues.append(f'contradiction_{i}_unmatched_claimed_as_established')
        if not detail(conf.get('comparability_check')): issues.append(f'contradiction_{i}_no_fair_comparison')
    if not detail(card.get('scope_limits')):issues.append('missing_source_and_scope_limits')
    if not detail(card.get('reproduction_first_action')):issues.append('no_actionable_asset_or_fairness_check')
    issues=sorted(set(issues))
    return {'ready':not issues,'status':'PAPER_ANCHOR_STRUCTURAL_READY' if not issues else 'PAPER_ANCHOR_NEEDS_EVIDENCE',
            'issues':issues,'paper_count':len(papers),'located_evidence_count':located,
            'note':'Checks schema and self-reported evidence only, not article accuracy, real availability, scientific impact or novelty.'}

def main():
    pa=argparse.ArgumentParser(description=__doc__);pa.add_argument('--input',required=True)
    args=pa.parse_args();r=assess(json.loads(Path(args.input).read_text(encoding='utf8')))
    print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['ready'] else 2
if __name__=='__main__':raise SystemExit(main())
