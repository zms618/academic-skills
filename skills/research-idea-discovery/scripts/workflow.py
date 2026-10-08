#!/usr/bin/env python3
"""Offline research workflow presence-gate checker, NOT a substitute for academic evaluation.

Two loops: IDEA_SELECTION then PAPER_ARGUMENT. Each checker evaluates record
presence and reported status; it cannot validate datasets, papers or reviewers.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path
try:
    from scripts.argument_audit import (audit_motivation, audit_story, audit_logic,
                                         audit_motivation_recheck, audit_novelty)
    from scripts.dataset_anchor import assess_anchor
    from scripts.feasibility_check import assess_feasibility
    from scripts.dataset_access import verify_sample
    from scripts.execution_evidence import review_record, pilot_record
    from scripts.literature_coverage import report as coverage_report
except ModuleNotFoundError:
    from argument_audit import (audit_motivation, audit_story, audit_logic,
                                 audit_motivation_recheck, audit_novelty)
    from dataset_anchor import assess_anchor
    from feasibility_check import assess_feasibility
    from dataset_access import verify_sample
    from execution_evidence import review_record, pilot_record
    from literature_coverage import report as coverage_report

STAGES=['SCOPE','SEARCH','EXPLAIN','DIVERGE','DATA_SEARCH','DATA_ANCHOR','FEASIBILITY',
        'MOTIVATION_INITIAL','FREEZE','SCOOP','MECHANISM_LOGIC','MOTIVATION_RECHECK',
        'NARRATIVE','REVIEW','PILOT','UPDATE']
CHECKS={
    'FEASIBILITY':('dataset_access_result.json','access_ready','D0: a dataset card/URL is not evidence of readable sample bytes and schema'),
    'MOTIVATION_INITIAL':('feasibility_result.json','precheck_ready','G0: full feasibility not established'),
    'FREEZE':('motivation_initial_result.json','ready','M1: initial motivation lacks evidence'),
    'MECHANISM_LOGIC':('novelty_result.json','ready','N: prior-art mechanism audit not ready'),
    'MOTIVATION_RECHECK':('logic_result.json','ready','L: mechanism necessity/logic not established'),
    'NARRATIVE':('motivation_recheck_result.json','ready','M2: revised motivation was not validated against prior work'),
    'REVIEW':('narrative_result.json','ready','S: scientific story/claim map not yet auditable'),
    'PILOT':('review_result.json','ready','REVIEW: no recorded and resolved reviewer decision to authorize pilot'),
    'UPDATE':('pilot_result.json','ready','PILOT: no real run log and result/failure evidence; stay PILOT_PLANNED'),
}
LEGACY_STAGE_MAP={'MOTIVATION':'MOTIVATION_INITIAL'}
INVALIDATED=['feasibility_result.json','motivation_initial_result.json','novelty_result.json',
             'logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json',
             'motivation_initial_result.json.input.json','novelty_result.json.input.json','logic_result.json.input.json',
             'motivation_recheck_result.json.input.json','narrative_result.json.input.json',
             'review_result.json','pilot_result.json']

def read_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def validate_stage_evidence(p, stage):
    """Replay local artifact checks rather than trusting an editable ready=true flag."""
    if stage=='FEASIBILITY':
        manifest=p/'dataset_access_manifest.json'
        anchor=p/'dataset_anchor_result.json'
        return (manifest.is_file() and anchor.is_file() and read_json(anchor).get('anchor_ready')
                and verify_sample(read_json(manifest)).get('access_ready'))
    if stage=='MECHANISM_LOGIC':
        record=p/'literature_search_record.json'
        return record.is_file() and coverage_report(read_json(record)).get('status')=='STRUCTURED_SEARCH_LOG_PRESENT'
    if stage=='PILOT':
        source=p/'review_card.json'
        if not source.exists():return False
        evaluated=review_record(read_json(source))
        original=read_json(p/'review_result.json') if (p/'review_result.json').exists() else {}
        return bool(evaluated.get('ready') and evaluated==original)
    if stage=='UPDATE':
        reference=p/'pilot_artifact_paths.json'
        if not reference.exists():return False
        info=read_json(reference)
        current=pilot_record(info.get('run_dir',''),info.get('metrics'))
        original=read_json(p/'pilot_result.json') if (p/'pilot_result.json').exists() else {}
        return bool(current.get('ready') and current==original)
    return True

def check_idea(idea):
    if not isinstance(idea,dict):idea={}
    required=['idea_id','revision','problem','hypothesis','falsifier','mechanism','unique_prediction',
              'naive_baseline','closest_prior_work','pilot','sources','dataset_anchor','feasibility',
              'motivation_initial','novelty','mechanism_logic','motivation_recheck','story']
    missing=[k for k in required if not idea.get(k)]
    if not isinstance(idea.get('closest_prior_work',[]),list):missing.append('closest_prior_work list')
    if not isinstance(idea.get('sources',[]),list):missing.append('sources list')
    feasibility=assess_feasibility(idea.get('feasibility'))
    anchor=assess_anchor(idea.get('dataset_anchor'))
    novelty=audit_novelty(idea.get('novelty'))
    logic=audit_logic(idea.get('mechanism_logic'))
    motivation_recheck=audit_motivation_recheck(idea.get('motivation_recheck'))
    checks={
        'D0_existing_dataset_anchor':anchor['anchor_ready'],
        'D0_sample_access': isinstance(idea.get('dataset_access'),dict) and idea['dataset_access'].get('access_ready') is True,
        'G0_feasibility':feasibility['precheck_ready'],
        'G1_hypothesis':bool(idea.get('problem') and idea.get('hypothesis') and idea.get('falsifier')),
        'G2_prior_art':novelty['ready'],
        'G3_rival':bool(idea.get('naive_baseline') and idea.get('unique_prediction')) and logic['ready'],
        'G4_test':isinstance(idea.get('pilot'),dict) and bool(idea['pilot'].get('kill_signal')),
        'G5_sources_fulltext':bool(idea.get('sources')) and isinstance(idea.get('sources'),list) and
                               all(isinstance(src,dict) and src.get('evidence_level') in ('E2','E3') for src in idea.get('sources',[])),
        'G6_resources':bool(idea.get('resources_checked')),
        'M1_initial_motivation':audit_motivation(idea.get('motivation_initial'))['ready'],
        'N_novelty_audit':novelty['ready'],
        'L_mechanism_logic':logic['ready'],
        'M2_motivation_recheck':motivation_recheck['ready'],
        'S_story_review':audit_story(idea.get('story'))['ready'],
    }
    # Academic conclusions must refer to the same idea/revision; copy-pasting
    # a prior assessment of another proposal is not an acceptable second pass.
    for name,data in [('novelty',idea.get('novelty')),('mechanism_logic',idea.get('mechanism_logic')),
                      ('motivation_recheck',idea.get('motivation_recheck'))]:
        if not isinstance(data,dict) or data.get('idea_id') != idea.get('idea_id') or data.get('revision') != idea.get('revision'):
            checks[{'novelty':'N_novelty_audit','mechanism_logic':'L_mechanism_logic','motivation_recheck':'M2_motivation_recheck'}[name]]=False
    checks['G2_prior_art']=checks['N_novelty_audit']
    checks['G3_rival']=checks['G3_rival'] and checks['L_mechanism_logic']
    return {'missing_fields':sorted(set(missing)),'gate_presence':checks,'feasibility_precheck':feasibility,
            'dataset_anchor_precheck':anchor,
            'status':'READY_FOR_HUMAN_REVIEW' if not missing and all(checks.values()) else 'EVIDENCE_OR_FIELDS_MISSING',
            'disclaimer':'Structural checks only; no assertion of novelty, persuasion or reproducibility.'}

def clear_downstream(p,st,from_stage,reason):
    for name in INVALIDATED:
        (p/name).unlink(missing_ok=True)
    if STAGES.index(st['stage'])>STAGES.index(from_stage):
        st['history'].append({'from':st['stage'],'to':from_stage,'reason':reason,
                             'when_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
        st['stage']=from_stage


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='cmd',required=True)
    init=sub.add_parser('init');init.add_argument('--project',required=True);init.add_argument('--domain',default='OPEN');init.add_argument('--goal',default='UNSPECIFIED')
    audit=sub.add_parser('audit');audit.add_argument('--project',required=True);audit.add_argument('--idea',required=True)
    advance=sub.add_parser('advance');advance.add_argument('--project',required=True);advance.add_argument('--stage',choices=STAGES,required=True);advance.add_argument('--reason',required=True)
    dv=sub.add_parser('dataset-verify');dv.add_argument('--project',required=True);dv.add_argument('--manifest',required=True)
    rv=sub.add_parser('record-review');rv.add_argument('--project',required=True);rv.add_argument('--card',required=True)
    pv=sub.add_parser('record-pilot');pv.add_argument('--project',required=True);pv.add_argument('--run-dir',required=True);pv.add_argument('--metrics')
    cv=sub.add_parser('literature-coverage');cv.add_argument('--project',required=True);cv.add_argument('--manifest',required=True)
    for cmd in ('dataset-anchor','feasibility','motivation-initial','motivation','novelty','logic','motivation-recheck','narrative'):
        a=sub.add_parser(cmd);a.add_argument('--project',required=True);a.add_argument('--card',required=True)
    status=sub.add_parser('status');status.add_argument('--project',required=True)
    a=parser.parse_args(argv);p=Path(a.project);fp=p/'workflow_state.json'
    if a.cmd=='init':
        if fp.exists():raise SystemExit('Project exists; will not erase prior research')
        write_json(fp,{'domain':a.domain,'goal':a.goal,'stage':'SCOPE','history':[],
            'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'dataset_policy':'IDEA_FIRST_AGENT_DISCOVERY_EXISTING_OR_DERIVED_ONLY',
            'argument_protocol':'M1_N_L_M2_S','evidence_status':'UNVERIFIED','role_mode':'ROLE_SIMULATED'})
        print(fp);return 0
    if not fp.exists():raise SystemExit('Project not initialized')
    st=read_json(fp)
    if st.get('stage') in LEGACY_STAGE_MAP:
        old=st['stage'];st['stage']=LEGACY_STAGE_MAP[old]
        clear_downstream(p,st,'FEASIBILITY','v2.5 review-order migration: invalidated old narrative assumptions')
        st['history'].append({'from':old,'to':st['stage'],'reason':'v2.5 order migration: previous motivation was post-novelty; re-audit required'})
        write_json(fp,st)
    if a.cmd=='status':print(json.dumps(st,indent=2,ensure_ascii=False));return 0
    if a.cmd=='dataset-verify':
        card=read_json(a.manifest)
        old=p/'dataset_access_manifest.json'
        if old.is_file() and read_json(old)!=card:
            clear_downstream(p,st,'DATA_ANCHOR','dataset sample or field requirements changed; rerun G0 and all later checks')
            write_json(fp,st)
        result=verify_sample(card)
        write_json(p/'dataset_access_manifest.json',card)
        write_json(p/'dataset_access_result.json',result)
        print(result['status']);return 0 if result['access_ready'] else 2
    if a.cmd=='record-review':
        if STAGES.index(st['stage'])<STAGES.index('REVIEW'):raise SystemExit('Review evidence cannot be submitted before REVIEW')
        card=read_json(a.card)
        previous=p/'review_card.json'
        if previous.is_file() and read_json(previous)!=card:
            (p/'pilot_result.json').unlink(missing_ok=True)
            (p/'pilot_artifact_paths.json').unlink(missing_ok=True)
            if STAGES.index(st['stage'])>STAGES.index('REVIEW'):
                st['stage']='REVIEW';write_json(fp,st)
        novelty=p/'novelty_result.json'
        if not novelty.is_file() or any(card.get(k)!=read_json(novelty).get(k) for k in ('idea_id','revision')):
            raise SystemExit('Review and novelty decision refer to different Idea ID/revision')
        result=review_record(card)
        write_json(p/'review_card.json',card)
        write_json(p/'review_result.json',result)
        print(result['status']);return 0 if result['ready'] else 2
    if a.cmd=='record-pilot':
        if STAGES.index(st['stage'])<STAGES.index('PILOT'):raise SystemExit('Pilot evidence cannot be submitted before PILOT')
        result=pilot_record(a.run_dir,a.metrics)
        write_json(p/'pilot_artifact_paths.json',{'run_dir':str(Path(a.run_dir).resolve()),
                                              'metrics':str(Path(a.metrics).resolve()) if a.metrics else None})
        write_json(p/'pilot_result.json',result)
        if result.get('requires_reaudit'):
            st['needs_reaudit']=True
            st['reaudit_reason']='Pilot failed or simplest baseline equivalent/better; revisit necessity, motivation and story'
            write_json(fp,st)
        print(result['status']);return 0 if result['ready'] else 2
    if a.cmd=='literature-coverage':
        card=read_json(a.manifest)
        prev=p/'literature_search_record.json'
        if prev.is_file() and read_json(prev)!=card and STAGES.index(st['stage'])>STAGES.index('SCOOP'):
            for name in ('novelty_result.json','logic_result.json','motivation_recheck_result.json',
                         'narrative_result.json','review_result.json','pilot_result.json'):
                (p/name).unlink(missing_ok=True)
            st['stage']='SCOOP';write_json(fp,st)
        result=coverage_report(card)
        write_json(p/'literature_search_record.json',card)
        write_json(p/'literature_coverage_result.json',result)
        print(result['status']);return 0 if result['status']=='STRUCTURED_SEARCH_LOG_PRESENT' else 2
    if a.cmd=='dataset-anchor':
        card=read_json(a.card);result=assess_anchor(card);old=p/'dataset_anchor_card.json'
        if not old.exists() or read_json(old)!=card:
            clear_downstream(p,st,'DATA_ANCHOR','dataset changed; all downstream decisions invalidated')
            write_json(fp,st)
        (p/'dataset_access_result.json').unlink(missing_ok=True)
        (p/'dataset_access_manifest.json').unlink(missing_ok=True)
        write_json(old,card);write_json(p/'dataset_anchor_result.json',result)
        print(result['status']);return 0 if result['anchor_ready'] else 2
    funcs={'feasibility':(assess_feasibility,'feasibility_result.json','precheck_ready'),
           'motivation-initial':(audit_motivation,'motivation_initial_result.json','ready'),
           'motivation':(audit_motivation,'motivation_initial_result.json','ready'),
           'novelty':(audit_novelty,'novelty_result.json','ready'),
           'logic':(audit_logic,'logic_result.json','ready'),
           'motivation-recheck':(audit_motivation_recheck,'motivation_recheck_result.json','ready'),
           'narrative':(audit_story,'narrative_result.json','ready')}
    if a.cmd in funcs:
        fn,out,flag=funcs[a.cmd]
        required_phase={'motivation-initial':'MOTIVATION_INITIAL','motivation':'MOTIVATION_INITIAL',
                        'novelty':'SCOOP','logic':'MECHANISM_LOGIC',
                        'motivation-recheck':'MOTIVATION_RECHECK','narrative':'NARRATIVE'}
        phase=required_phase.get(a.cmd)
        if phase and STAGES.index(st['stage'])<STAGES.index(phase):
            raise SystemExit(f'{a.cmd} cannot be submitted before {phase}')
        card=read_json(a.card)
        snapshot=p/(out+'.input.json')
        if snapshot.exists() and read_json(snapshot)!=card:
            # A genuinely revised argument invalidates all later assessments.
            invalidation={
                'motivation-initial':['novelty_result.json','logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json'],
                'motivation':['novelty_result.json','logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json'],
                'novelty':['logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json'],
                'logic':['motivation_recheck_result.json','narrative_result.json','audit_result.json'],
                'motivation-recheck':['narrative_result.json','audit_result.json'],
                'narrative':['audit_result.json']}
            for filename in invalidation.get(a.cmd,[]):
                (p/filename).unlink(missing_ok=True)
            reset_phase={
                'motivation-initial':'MOTIVATION_INITIAL','motivation':'MOTIVATION_INITIAL',
                'novelty':'SCOOP','logic':'MECHANISM_LOGIC',
                'motivation-recheck':'MOTIVATION_RECHECK','narrative':'NARRATIVE'}[a.cmd]
            if STAGES.index(st['stage'])>STAGES.index(reset_phase):
                st['history'].append({'from':st['stage'],'to':reset_phase,
                    'reason':'audit input changed; invalidate downstream assessments'})
                st['stage']=reset_phase;write_json(fp,st)
        if a.cmd in ('logic','motivation-recheck'):
            base=p/'novelty_result.json'
            nv=read_json(base) if base.exists() else {}
            if not nv.get('ready') or nv.get('idea_id')!=card.get('idea_id') or nv.get('revision')!=card.get('revision'):
                raise SystemExit('Idea ID/revision mismatch or novelty not verified for this exact idea')
        result=fn(card)
        write_json(snapshot,card)
        write_json(p/out,result)
        print(result['status']+' -> '+str(p/out));return 0 if result[flag] else 2
    if a.cmd=='audit':
        r=check_idea(read_json(a.idea));out=p/'audit_result.json';write_json(out,r)
        print(r['status']+' -> '+str(out));return 0 if r['status']=='READY_FOR_HUMAN_REVIEW' else 2
    cur=STAGES.index(st['stage']);tar=STAGES.index(a.stage)
    if tar>cur+1:raise SystemExit('Cannot skip scientific stages')
    # Check conditions on arrival at each stage. No stage can replace evidence with a flattering score.
    if tar>cur:
        if a.stage in CHECKS:
            filename,flag,message=CHECKS[a.stage]
            path=p/filename
            if not path.exists() or not read_json(path).get(flag,False): raise SystemExit(message)
        if a.stage in ('FEASIBILITY','MECHANISM_LOGIC','PILOT','UPDATE') and not validate_stage_evidence(p,a.stage):
            raise SystemExit(a.stage+': underlying source artifact missing, stale, or invalid')
    if tar<cur:
        # Revisions invalidate research conclusions from the point they are revised.
        if tar<=STAGES.index('FEASIBILITY'):
            clear_downstream(p,st,a.stage,'research assumption changed: '+a.reason)
        elif tar<=STAGES.index('MOTIVATION_INITIAL'):
            for name in ('motivation_initial_result.json','novelty_result.json','logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json'):(p/name).unlink(missing_ok=True)
        elif tar<=STAGES.index('SCOOP'):
            for name in ('novelty_result.json','logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json'):(p/name).unlink(missing_ok=True)
        elif tar<=STAGES.index('MECHANISM_LOGIC'):
            for name in ('logic_result.json','motivation_recheck_result.json','narrative_result.json','audit_result.json'):(p/name).unlink(missing_ok=True)
        else:
            for name in ('motivation_recheck_result.json','narrative_result.json','audit_result.json'):(p/name).unlink(missing_ok=True)
        if tar<=STAGES.index('REVIEW'):
            (p/'review_result.json').unlink(missing_ok=True)
            (p/'pilot_result.json').unlink(missing_ok=True)
    st['history'].append({'from':st['stage'],'to':a.stage,'reason':a.reason,
        'when_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    st['stage']=a.stage;write_json(fp,st);print('Stage -> '+a.stage);return 0

if __name__=='__main__':sys.exit(main())
