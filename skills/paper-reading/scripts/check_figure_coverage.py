#!/usr/bin/env python3
"""Audit a human/model-reviewed paper Figure/Table/Algorithm map.

Not a PDF parser or an image-display detector: a passing audit means the supplied
records are internally complete, not that their claims are true or a UI displayed.

Usage:
  python check_figure_coverage.py path/to/figure-plan.json --stage 1
"""
import argparse
import json
import sys
from pathlib import Path

ALLOWED_TYPES = {'figure', 'table', 'algorithm', 'teaser'}
ALLOWED_VISUALS = {'architecture', 'pipeline', 'algorithm', 'scenario', 'result', 'ablation', 'dataset', 'diagnostic', 'other'}
METHOD_KINDS = {'architecture', 'pipeline_only', 'algorithm_only', 'none'}


def audit_plan(plan, stage):
    """Return clear audit errors; no hardcoded paper title or figure numbers."""
    if not isinstance(plan, dict):
        return ['plan must be a JSON object']
    errors = []
    if type(stage) is not int or not 1 <= stage <= 7:
        return ['stage must be an integer from 1 to 7']
    assets = plan.get('assets')
    if not isinstance(assets, list) or not assets:
        return ['assets must be a nonempty list built from the actual paper']
    ids = set()
    required = []
    for i, a in enumerate(assets):
        if not isinstance(a, dict):
            errors.append(f'asset {i}: must be an object')
            continue
        aid = str(a.get('id', '')).strip()
        if not aid or aid in ids:
            errors.append(f'asset {i}: missing or duplicate id {aid!r}')
        ids.add(aid)
        if a.get('kind') not in ALLOWED_TYPES:
            errors.append(f'{aid}: invalid kind')
        if a.get('visual_type') not in ALLOWED_VISUALS:
            errors.append(f'{aid}: invalid visual_type')
        if type(a.get('pdf_page')) is not int or a['pdf_page'] < 1:
            errors.append(f'{aid}: missing verified pdf_page')
        for k in ('caption', 'visually_observed', 'body_reference', 'argument_role', 'why_required'):
            if not isinstance(a.get(k), str) or not a[k].strip():
                errors.append(f'{aid}: missing evidence field {k}')
        assigned = a.get('required_stages')
        if not isinstance(assigned, list) or not all(type(x) is int and 1 <= x <= 7 for x in assigned):
            errors.append(f'{aid}: invalid required_stages')
            assigned = []
        if stage in assigned:
            required.append(aid)
        if type(a.get('first_stage')) is int and assigned and a['first_stage'] != min(assigned):
            errors.append(f'{aid}: first_stage contradicts required_stages')
        revisit = a.get('revisit_stages', [])
        if not isinstance(revisit, list) or any(type(s) is not int or s not in range(1, 8) for s in revisit):
            errors.append(f'{aid}: invalid revisit_stages')
    stage_audit = plan.get('stage_audit', {})
    if not isinstance(stage_audit, dict):
        errors.append('stage_audit must be an object')
        stage_audit = {}
    logs = stage_audit.get(str(stage), {})
    if not isinstance(logs, dict):
        errors.append(f'stage_audit[{stage}] must be an object')
        logs = {}
    for aid in required:
        entry = logs.get(aid, {})
        if not isinstance(entry, dict):
            errors.append(f'{aid}: stage audit entry must be an object')
            continue
        if entry.get('display_attempted') is not True or entry.get('explained') is not True:
            errors.append(f'{aid}: required evidence not both displayed/attempted and explained in stage {stage}')
    links = plan.get('required_links', [])
    if not isinstance(links, list):
        errors.append('required_links must be a list')
        links = []
    for link in links:
        if not isinstance(link, dict):
            errors.append('required_links entries must be objects')
            continue
        if link.get('from') not in ids or link.get('to') not in ids:
            errors.append('required_links: references unknown asset')
        if link.get('stage') == stage:
            if not link.get('why') or not link.get('explained'):
                errors.append(f"{link.get('from')} -> {link.get('to')}: required cross-figure logic not explained")
    if stage == 2:
        method = plan.get('method_overview', {})
        if not isinstance(method, dict):
            errors.append('method_overview must be an object')
            method = {}
        kind = method.get('type')
        if kind not in METHOD_KINDS:
            errors.append('stage 2: method figure type unverified (architecture/pipeline_only/algorithm_only/none)')
        if method.get('explicitly_declared') is not True:
            errors.append('stage 2: method figure presence/absence not explicitly declared to reader')
        if method.get('input_output_explained') is not True or method.get('intuitive_flow_explained') is not True:
            errors.append('stage 2: intuitive input/output and method flow not both explained')
        if kind == 'architecture' and not any(a['visual_type'] == 'architecture' for a in assets):
            errors.append('stage 2: architecture declared but no verified architecture asset')
        if kind == 'algorithm_only' and not any(a['kind'] == 'algorithm' for a in assets):
            errors.append('stage 2: algorithm-only claimed but Algorithm asset missing')
        if kind in {'algorithm_only', 'pipeline_only', 'none'} and method.get('lack_of_architecture_stated') is not True:
            errors.append('stage 2: must state no separate network architecture diagram')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--stage', type=int, required=True)
    args = parser.parse_args()
    data = json.loads(args.plan.read_text(encoding='utf-8'))
    errors = audit_plan(data, args.stage)
    if errors:
        for e in errors:
            print('INCOMPLETE:', e)
        print('Remain in current stage; DO NOT offer next-stage button.')
        return 1
    print(f'PASS: stage {args.stage} essential evidence and checks covered according to supplied audit. UI visibility not verified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
