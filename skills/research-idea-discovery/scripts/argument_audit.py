#!/usr/bin/env python3
"""Offline claim/argument *presence* gate, not an AI reviewer or empirical verifier."""
import argparse
import json
from pathlib import Path

MOTIVATION_KEYS=('failure_observation','failure_evidence','scientific_stakes','hidden_assumption',
                 'competing_explanations','strong_baseline_limit','why_now','hypothesis','falsifier','unique_prediction')
STORY_KEYS=('hook','status_quo','observed_gap','root_cause','central_insight','mechanism',
            'novelty_delta','discriminating_experiment','scope_and_limits','pitch_30s','intro_outline',
            'claim_evidence_map','review_rounds')
REVIEW_ROUNDS=('M','N','R')

def nonempty(x):
    return (bool(x.strip()) if isinstance(x,str) else bool(x))

def supported_sources(items):
    # Only checks presence of source records and reported evidence grade, not their authenticity.
    if not isinstance(items,list) or not items: return False
    return any(isinstance(s,dict) and nonempty(s.get('source')) and nonempty(s.get('locator')) and
               s.get('evidence_level') in ('E2','E3','USER_OBSERVATION_VERIFIABLE') for s in items)

def audit_motivation(card):
    if not isinstance(card,dict): card={}
    missing=[k for k in MOTIVATION_KEYS if not nonempty(card.get(k))]
    if not isinstance(card.get('competing_explanations'),list) or len(card.get('competing_explanations',[]))<2:
        missing.append('competing_explanations >= 2')
    if not supported_sources(card.get('sources')):missing.append('locatable evidence (E2/E3/user-verifiable)')
    if card.get('problem_status') == 'CONTRADICTED': return {'status':'MOTIVATION_REJECTED','ready':False,'missing':missing}
    return {'status':'MOTIVATION_EVIDENCE_PRESENT' if not missing else 'MOTIVATION_UNVERIFIED',
            'ready':not missing,'missing':sorted(set(missing)),
            'warning':'Syntactic evidence-presence check only; importance, causality and truth require real reading/validation.'}

def audit_story(card):
    if not isinstance(card,dict):card={}
    missing=[k for k in STORY_KEYS if not nonempty(card.get(k))]
    claimmap=card.get('claim_evidence_map')
    if not isinstance(claimmap,list) or not claimmap or any(not isinstance(c,dict) or not all(nonempty(c.get(k)) for k in ('claim','evidence_or_experiment','status')) for c in claimmap):
        missing.append('claim_evidence_map with claim/evidence_or_experiment/status')
    rounds=card.get('review_rounds')
    if not isinstance(rounds,list):rounds=[]
    observed={r.get('round'):r for r in rounds if isinstance(r,dict)}
    for name in REVIEW_ROUNDS:
        r=observed.get(name)
        if r is None or any(not nonempty(r.get(k)) for k in ('attack','response','new_evidence_or_mechanism_delta','decision')):
            missing.append('review_round_'+name)
        elif r.get('decision') in ('STOP','REJECT','UNRESOLVED','REVISE','REQUEST_EVIDENCE') or r.get('critical_objection_unresolved') is True:
            missing.append('unresolved_core_objection_round_'+name)
    if card.get('claim_verdict') == 'CONTRADICTED': missing.append('contradicted key claim')
    if isinstance(claimmap,list) and any(isinstance(c,dict) and c.get('status')=='CONTRADICTED' for c in claimmap):
        missing.append('claim evidence contains contradicted core claim')
    if card.get('closest_prior_status') in ('COLLISION_CONFIRMED','HIGH_RISK'):missing.append('unresolved prior-art collision')
    return {'status':'STORY_STRUCTURE_READY_FOR_REVIEW' if not missing else 'STORY_REVISE',
            'ready':not missing,'missing':sorted(set(missing)),
            'warning':'Only field presence and declared review-round coverage checked; narrative persuasiveness is not automatically proven.'}

LOGIC_KEYS=('problem_cause','intervention','causal_bridge','strongest_prior_mechanism',
            'simple_rival','rival_distinction','necessity_ablation','unique_prediction',
            'discriminating_test','confounders','failure_boundary')
RECHECK_KEYS=('original_problem_claim','closest_prior_work', 'prior_work_explains',
             'remaining_gap', 'importance_after_prior_art', 'revised_central_claim',
             'distinctive_prediction', 'new_falsifier', 'revision_rationale')


def audit_logic(card):
    """Check documented necessity/logic arguments; not causal proof."""
    if not isinstance(card,dict):card={}
    missing=[k for k in LOGIC_KEYS if not nonempty(card.get(k))]
    if not isinstance(card.get('confounders'),list) or not card['confounders']:
        missing.append('confounders as nonempty list')
    if card.get('simple_rival_outcome') == 'EQUIVALENT_OR_BETTER':
        missing.append('simple rival already explains outcome; mechanism necessity not established')
    if card.get('mechanism_status') in ('CONTRADICTED','EQUIVALENT_TO_PRIOR'):
        missing.append('mechanism falsified or functionally equivalent')
    return {'status':'LOGIC_ARGUMENT_PRESENT' if not missing else 'LOGIC_REVISE',
            'ready':not missing,'missing':sorted(set(missing)),
            'warning':'Presence check only, not proof that the mechanism causes gains.'}


def audit_motivation_recheck(card):
    """Require post-novelty re-assessment of the *same* question, not new storytelling."""
    if not isinstance(card,dict):card={}
    missing=[k for k in RECHECK_KEYS if not nonempty(card.get(k))]
    if not supported_sources(card.get('sources')):missing.append('locatable sources of reconsidered problem')
    if card.get('novelty_status') in ('COLLISION_CONFIRMED','HIGH_RISK','NOVELTY_UNVERIFIED'):
        missing.append('unresolved near-prior collision or novelty uncertainty')
    if card.get('gap_status') in ('COVERED','CONTRADICTED'):
        missing.append('post-prior motivation no longer holds')
    # Deliberately require specific consequences of reading the neighbor; copy-pasting
    # the initial motivation unchanged must not be misrepresented as a second check.
    if card.get('revision_rationale') in ('no change','unchanged','same as before'):
        missing.append('recheck does not account for prior work')
    return {'status':'MOTIVATION_RECHECK_PRESENT' if not missing else 'MOTIVATION_RECHECK_FAILED',
            'ready':not missing,'missing':sorted(set(missing)),
            'warning':'Only structure is checked; citations and validity of the revised gap need real scholarly review.'}


def audit_novelty(card):
    """Structured prior-art minimum: source methods are verified by researchers, not code."""
    if not isinstance(card,dict): card={}
    required=('idea_id','revision','novelty_verdict','novelty_delta','unique_prediction','closest_prior_work')
    missing=[k for k in required if not nonempty(card.get(k))]
    prior=card.get('closest_prior_work')
    if not isinstance(prior,list) or not prior:
        missing.append('closest_prior_work list')
    else:
        for i,entry in enumerate(prior):
            if not isinstance(entry,dict) or any(not nonempty(entry.get(k)) for k in ('title','source','method_locator','mechanism','overlap','difference','evidence_level')):
                missing.append(f'closest_prior_work[{i}] source, locator and six-axis mechanism details')
            elif entry.get('evidence_level') not in ('E2','E3'):
                missing.append(f'closest_prior_work[{i}] no full method verification')
    if card.get('novelty_verdict') != 'PROVISIONALLY_DIFFERENTIATED':
        missing.append('novelty collision/unverified status')
    return {'status':'NOVELTY_STRUCTURE_READY' if not missing else 'NOVELTY_NOT_READY',
            'ready':not missing,'missing':sorted(set(missing)),
            'idea_id':card.get('idea_id'),'revision':card.get('revision'),
            'novelty_verdict':card.get('novelty_verdict'),
            'warning':'Presence check cannot prove academic originality or the quality of a novelty delta.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=('motivation','story','logic','motivation-recheck','novelty'));parser.add_argument('--card',required=True)
    parser.add_argument('--out')
    a=parser.parse_args(argv)
    card=json.loads(Path(a.card).read_text(encoding='utf-8'))
    result={'motivation':audit_motivation,'story':audit_story,'logic':audit_logic,'motivation-recheck':audit_motivation_recheck,'novelty':audit_novelty}[a.kind](card)
    if a.out:
        path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['ready'] else 2
if __name__=='__main__': raise SystemExit(main())
