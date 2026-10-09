#!/usr/bin/env python3
"""Offline structural audit for optional machine-readable advisor reports.

This checks only presence, statuses, and self-consistency. It does not verify scientific
novelty, official datasets, code availability or execution claims.
"""
import argparse
import json

METHOD_STATUSES={"DESIGN_PROPOSED","METHOD_NOT_READY","IMPLEMENTATION_VERIFIED","EXECUTED_WITH_LOGS"}
from pathlib import Path

STATUSES={"PROMISING_SEED","CONDITIONAL_CANDIDATE","STRONG_CANDIDATE","NEEDS_EVIDENCE","HIGH_RISK","REJECT","NO_DEFENSIBLE_IDEA_FOUND"}
ACTIONS={"GO_E0","REFINE","PIVOT","STOP","RESEARCH_MORE"}

def audit(report):
    issues=[]
    if not isinstance(report,dict):return ["report must be JSON object"]
    status=report.get("status")
    if status not in STATUSES:issues.append("status must be valid")
    if report.get("action") not in ACTIONS:issues.append("action must be valid")
    # v3.4: broad research needs a landscape and a gap-stage report before method promises.
    if report.get('protocol_version')=='3.4' and report.get('report_phase')=='MOTIVATION_PORTFOLIO':
        for key in ('motivation_landscape','source_coverage','comparative_shortlist','counterevidence','next_evidence_action'):
            if not report.get(key):issues.append('portfolio early report missing '+key)
        for key in ('method_design','potential_contributions','new_architecture','loss_function'):
            if report.get(key):issues.append('portfolio must not include premature '+key)
        return issues
    if report.get('protocol_version')=='3.4' and report.get('report_phase')=='SHORTLISTED_GAP':
        for key in ('motivation_landscape','shortlisted_gap_reports','source_coverage','no_survivor_fallback'):
            if not report.get(key):issues.append('gap-stage report missing '+key)
        if not report.get('gap_ready'):
            for key in ('method_design','potential_contributions','new_architecture','loss_function'):
                if report.get(key):issues.append('unresolved gap cannot contain '+key)
        return issues
    # Motivation first: weak problem means STOP the expensive downstream report.
    if report.get('protocol_version') == '3.3' and report.get('report_phase') == 'M0_PROBLEM_DISCOVERY':
        gate=report.get('motivation_gate')
        if not isinstance(gate,dict) or gate.get('status') not in ('PROBE_ONLY','REJECT_OR_REFRAME','RESEARCH_MORE'):
            issues.append('early report must name non-passing M0 verdict')
        for field in ('problem_evidence_card','next_evidence_action','problem_importance','alternative_explanations'):
            if not report.get(field):issues.append('M0 early report missing '+field)
        for field in ('method_design','potential_contributions','new_architecture','loss_function'):
            if report.get(field):issues.append('M0 non-pass report must not propose '+field)
        return issues
    if report.get('protocol_version') == '3.4':
        if not report.get('motivation_landscape') or not report.get('shortlisted_gap_reports'):
            issues.append('v3.4 report requires preceding motivation portfolio and shortlisted gaps')
        if report.get('gap_status')!='PROVISIONAL_GAP_READY':
            issues.append('v3.4 full report requires provisional unresolved gap')
    if report.get('protocol_version') in ('3.3','3.4'):
        gate=report.get('motivation_gate')
        if not isinstance(gate,dict) or gate.get('status') != 'PASS_FOR_IDEATION':
            issues.append('full v3.3+ report requires M0 PASS_FOR_IDEATION')
        if not report.get('problem_evidence_card'):
            issues.append('full v3.3+ report requires problem evidence card')
    if report.get('protocol_version')=='3.4' and report.get('report_phase') not in ('MOTIVATION_PORTFOLIO','SHORTLISTED_GAP'):
        if 'CVPR' in str(report.get('goal','')).upper() and any(q in str(report.get('goal','')).upper() for q in ('BEST','最佳')):
            impact=report.get('cvpr_aspiration_review')
            fields=('vision_relevance','scientific_significance','potential_generalizable_insight',
                    'closest_conceptual_rival','unique_discriminating_experiment','technical_soundness_risk',
                    'expected_real_world_or_field_impact','reproducibility_limitations',
                    'bold_hypothesis_falsifier','award_claim_limit')
            if not isinstance(impact,dict) or any(not impact.get(k) for k in fields):
                issues.append('CVPR Best Paper aspiration needs evidence-specific impact review; cannot replace this with numerical award score')
            elif 'guaranteed' in str(impact.get('award_claim_limit','')).lower():
                issues.append('Never claim Best Paper is guaranteed')
    if status in {"NO_DEFENSIBLE_IDEA_FOUND","REJECT"}:
        for field in ("rejected_reasons","missing_evidence","next_evidence_action"):
            if not report.get(field):issues.append("missing "+field)
        if status=="NO_DEFENSIBLE_IDEA_FOUND" and not report.get("deep_research_prompt"):
            issues.append("negative result requires targeted Deep Research prompt")
        return issues
    for field in ("plain_language_question","concrete_example","motivation","prior_work","hypothesis","potential_contributions","scientific_story","feasibility","first_48h","first_week","kill_criteria","reviewer_risks","teach_back"):
        if not report.get(field):issues.append("missing "+field)
    feats=report.get("feasibility")
    if isinstance(feats,dict):
        for field in ("dataset","model_checkpoint","baselines","data_access_status","evaluation_protocol"):
            if not feats.get(field):issues.append("feasibility missing "+field)
    elif feats is not None:issues.append("feasibility must be object")
    contribs=report.get("potential_contributions")
    if isinstance(contribs,list):
        if len(contribs)>3:issues.append("at most three proposed contributions")
        for i,cont in enumerate(contribs):
            if not isinstance(cont,dict) or not all(cont.get(k) for k in ("claim","status","required_evidence")):
                issues.append(f"contribution {i} missing claim/status/required_evidence")
            elif cont.get('status')=='VALIDATED' and not cont.get('verified_experiment_or_proof'):
                issues.append(f"contribution {i} claims VALIDATED without proven evidence reference")
    if status=='STRONG_CANDIDATE' and isinstance(feats,dict) and feats.get('data_access_status') in ('UNKNOWN','CATALOG_ONLY','BLOCKED','ACCESS_PENDING'):
        issues.append("STRONG_CANDIDATE incompatible with unknown/blocked data access")
    if isinstance(report.get('first_48h'),list) and len(report['first_48h'])<2:
        issues.append('first_48h requires concrete multi-step E0')
    if isinstance(report.get('kill_criteria'),list) and len(report['kill_criteria'])<2:
        issues.append('kill_criteria needs at least two falsifiers')
    if report.get('pilot_status')=='EXECUTED' and not report.get('pilot_log_reference'):
        issues.append('executed pilot requires log reference')
    # v3.2: scientific method viability is not optional in full candidate reports.
    if report.get('method_status') not in METHOD_STATUSES:
        issues.append('method_status missing/invalid')
    method=report.get('method_design')
    if not isinstance(method,dict):
        issues.append('method_design must be an object')
    else:
        track=method.get('track','DL')
        if track not in ('DL','NON_DL'):
            issues.append('method_design track invalid')
        fields=('task_io','baseline_decision','decision_rule','implementation_limitations','weakest_assumption','cost_scaling')
        fields+=(('estimator','loss_or_algorithm','frozen_parameters','updated_parameters','integration','update_timeline','test_label_policy','source_data_policy','shift_protocol','leakage_controls') if track=='DL' else ('operational_protocol','controls','falsifying_observation'))
        for field in fields:
            if not method.get(field):issues.append('method_design missing '+field)
        if track=='DL':
            est=method.get('estimator')
            if not isinstance(est,dict) or not all(est.get(k) for k in ('observables','formula_or_procedure','validation_test')):
                issues.append('estimator must name observables, formula_or_procedure and validation_test')
            inte=method.get('integration')
            if not isinstance(inte,dict) or not all(inte.get(k) for k in ('repo_url_or_status','entrypoint_status','first_function','input_contract','output_contract')):
                issues.append('integration requires repo, entrypoint, first function, input/output contract')
            tl=method.get('update_timeline')
            if not isinstance(tl,list) or len(tl)<2:
                issues.append('update_timeline needs t0 and t1 behavior')
    if report.get('method_status')=='IMPLEMENTATION_VERIFIED' and not report.get('implementation_test_log'):
        issues.append('IMPLEMENTATION_VERIFIED requires implementation_test_log')
    if report.get('method_status')=='EXECUTED_WITH_LOGS' and not (report.get('implementation_test_log') and report.get('pilot_log_reference') and report.get('pilot_metrics_reference')):
        issues.append('EXECUTED_WITH_LOGS requires implementation_test_log, pilot_log_reference and pilot_metrics_reference')
    trial=report.get('researcher_trial')
    if not isinstance(trial,dict) or not all(trial.get(k) for k in ('student_blockers','reviewer_attacks','fixes_applied','remaining_unknowns','simulation_status')):
        issues.append('researcher_trial requires student/reviewer blockers, fixes, unknowns and status')
    elif trial['simulation_status'] not in ('ROLE_SIMULATED','INDEPENDENT_RUN_VERIFIED'):
        issues.append('researcher_trial simulation status invalid')
    cards=report.get('action_cards')
    if not isinstance(cards,list) or len(cards)<3:
        issues.append('action_cards require at least three actionable research steps')
    else:
        for i,c in enumerate(cards):
            if not isinstance(c,dict) or not all(c.get(k) for k in ('prerequisite','action','artifact','interpretation')):
                issues.append(f'action_card {i} missing prerequisites/action/artifact/interpretation')
    if isinstance(contribs,list):
        for i,c in enumerate(contribs):
            if isinstance(c,dict) and not all(c.get(k) for k in ('nearest_prior','novelty_delta','distinguishing_test','necessity_ablation','kill_signal')):
                issues.append(f'contribution {i} missing independent novelty/necessity evidence')
        for field in ('novelty_delta','distinguishing_test'):
            values=[str(c.get(field,'')).lower().strip() for c in contribs if isinstance(c,dict) and c.get(field)]
            if len(values)!=len(set(values)):
                issues.append(f'contributions reuse identical {field}; merge or justify independent novelty')
    # Obvious generic filler never counts as an operational scientific proposal.
    if isinstance(method,dict):
        for field in ('decision_rule','weakest_assumption','implementation_limitations','loss_or_algorithm'):
            val=method.get(field)
            if isinstance(val,str) and val.strip().lower() in {'tbd','todo','novel framework','robust model','improve robustness','设计新模型','提高鲁棒性','提升性能','待补充'}:
                issues.append(f'method_design {field} is placeholder/empty jargon')
    if report.get('method_status')=='METHOD_NOT_READY' and report.get('status')=='STRONG_CANDIDATE':
        issues.append('STRONG_CANDIDATE incompatible with METHOD_NOT_READY')
    return issues

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');args=p.parse_args()
    report=json.loads(Path(args.input).read_text(encoding='utf-8'))
    issues=audit(report)
    output={'structure_complete':not bool(issues),'issues':issues,'note':'Structural audit only; does not validate scientific facts, novelty or URLs'}
    if args.output:Path(args.output).write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0 if not issues else 2
if __name__=='__main__':raise SystemExit(main())
