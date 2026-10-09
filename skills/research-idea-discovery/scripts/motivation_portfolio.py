#!/usr/bin/env python3
"""Structural motivation portfolio and scoped gap-audit checks.

None of these functions checks factual article contents or awards potential.
"""
import argparse
import json
from pathlib import Path

MATURE={'DIRECT_LOCATED','PRIMARY_LEAD','HYPOTHESIS_ONLY','COUNTEREVIDENCE'}
GAP_STATES={'SURVIVES_GAP','PROBE_ONLY','ALREADY_SOLVED','RESEARCH_MORE'}

def full(s):
    return isinstance(s,str) and len(s.strip())>=10 and s.strip().lower() not in ('tbd','unknown','n/a','none','提高鲁棒性','提升性能','best paper','新方法')

def assess_portfolio(card):
    if not isinstance(card,dict): card={}
    issues=[]
    motivations=card.get('motivations',[])
    if not isinstance(motivations,list): motivations=[]
    if len(motivations)<3: issues.append('portfolio_should_compare_three_or_more_distinct_problems')
    if len(motivations)>10: issues.append('portfolio_exceeds_bounded_search_budget')
    ids=[]; families=[]
    fields=('problem_id','failure_family','task_protocol','observed_or_hypothesized_failure',
        'scientific_importance','strong_simple_baseline','null_explanation','falsifier',
        'source_locator','cvpr_scope_argument')
    for i,m in enumerate(motivations):
        if not isinstance(m,dict): issues.append(f'invalid_motivation_{i}');continue
        ids.append(m.get('problem_id'))
        families.append(m.get('failure_family'))
        for k in fields:
            if not full(m.get(k)):issues.append(f'motivation_{i}_missing_{k}')
        if m.get('evidence_status') not in MATURE:issues.append(f'motivation_{i}_unknown_evidence_status')
        if any(k in m for k in ('architecture','loss','method_name','innovations')):
            issues.append(f'motivation_{i}_premature_method_first_fields')
    if len(set(ids))!=len(ids):issues.append('duplicate_problem_ids')
    if len(set(families))<min(3,len(motivations)):
        issues.append('problems_are_relabelled_variants_not_independent_motivations')
    shortlist=card.get('shortlist',[])
    if not isinstance(shortlist,list):shortlist=[]
    if not (1<=len(shortlist)<=3):issues.append('shortlist_must_have_one_to_three_justified_problems')
    if len(motivations)>=5 and len(shortlist)<2 and not full(card.get('shortlist_exception')):
        issues.append('need_two_shortlist_motivations_or_explain_why_only_one')
    picked=[]
    for j,sel in enumerate(shortlist):
        if not isinstance(sel,dict):issues.append(f'shortlist_{j}_not_object');continue
        pid=sel.get('problem_id');picked.append(pid)
        if pid not in ids:issues.append(f'shortlist_{j}_not_in_portfolio')
        if not full(sel.get('why_selected_over_rival')):issues.append(f'shortlist_{j}_no_contrastive_justification')
        if not full(sel.get('most_dangerous_uncertainty')):issues.append(f'shortlist_{j}_no_falsifying_uncertainty')
    if len(set(picked))!=len(picked):issues.append('duplicate_shortlist_selection')
    if not full(card.get('search_scope_and_limits')):issues.append('missing_broad_search_coverage_and_limits')
    if not full(card.get('decision_caveat')):issues.append('missing_portfolio_is_not_novelty_or_award_proof_disclaimer')
    issues=sorted(set(issues))
    return {'ready':not issues,'status':'STRUCTURAL_PORTFOLIO_READY' if not issues else 'PORTFOLIO_REVISE',
            'issues':issues,'shortlisted_problem_ids':picked,
            'candidate_count':len(motivations),'distinct_families':len(set(families)),
            'note':'Presence/coherence check only; original sources, conceptual importance, CVPR eligibility and award potential NOT verified.'}

def assess_gap(card,portfolio):
    if not isinstance(card,dict):card={}
    picked=portfolio.get('shortlisted_problem_ids',[])
    rows=card.get('gap_findings',[])
    if not isinstance(rows,list):rows=[]
    issues=[]; indexed={}
    for i,g in enumerate(rows):
        if not isinstance(g,dict):issues.append('invalid_gap_finding');continue
        pid=g.get('problem_id')
        if pid in indexed: issues.append('duplicate_gap_problem_id')
        indexed[pid]=g
        if pid not in picked:issues.append('gap_finding_for_unshortlisted_problem')
        for k in ('known_explanation','unresolved_testable_question','dangerous_simple_rival',
                  'counterevidence','needed_discriminator','coverage_limit'):
            if not full(g.get(k)):issues.append(f'gap_{i}_missing_{k}')
        if g.get('status') not in GAP_STATES:issues.append(f'gap_{i}_invalid_status')
        literature=g.get('nearest_research',[])
        if not isinstance(literature,list) or not literature:
            issues.append(f'gap_{i}_missing_nearest_research')
        else:
            for paper in literature:
                if not isinstance(paper,dict) or not all(full(paper.get(k)) for k in ('title','source_url','actual_method_or_finding','reading_depth')):
                    issues.append(f'gap_{i}_incomplete_prior_evidence')
    if set(indexed)!=set(picked):issues.append('must_investigate_all_shortlisted_motivations_not_just_favorite')
    focus=card.get('focus_problem_id')
    if focus not in picked:issues.append('focus_problem_id_must_be_shortlisted')
    if focus in indexed and indexed[focus].get('status')!='SURVIVES_GAP':issues.append('focus_problem_has_no_provisional_unresolved_gap')
    if not full(card.get('why_focus_over_alternatives')):issues.append('missing_contrastive_focus_justification')
    issues=sorted(set(issues))
    return {'ready':not issues,'status':'PROVISIONAL_GAP_READY' if not issues else 'GAP_NEEDS_MORE_EVIDENCE',
        'issues':issues,'focus_problem_id':focus,'gap_review_count':len(rows),
        'note':'A complete source list is NOT a verified original contribution; independent prior-art and experiment checks remain mandatory.'}

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--mode',choices=['portfolio','gap'],default='portfolio')
    pa.add_argument('--input',required=True);pa.add_argument('--portfolio')
    x=pa.parse_args();card=json.loads(Path(x.input).read_text(encoding='utf8'))
    if x.mode=='portfolio': r=assess_portfolio(card)
    else:
        if not x.portfolio:pa.error('--portfolio needed for gap mode')
        p=assess_portfolio(json.loads(Path(x.portfolio).read_text(encoding='utf8')))
        r=assess_gap(card,p)
    print(json.dumps(r,ensure_ascii=False,indent=2))
    return 0 if r['ready'] else 2
if __name__=='__main__':raise SystemExit(main())
