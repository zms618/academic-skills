#!/usr/bin/env python3
"""Offline G0 resource-evidence precheck, NOT independent verification of actual resources.

No network calls, license validation, or actual dataset download. A syntactically
complete card still requires human/source-level verification to claim FEASIBLE_VERIFIED.
"""
import argparse
import json
from pathlib import Path

DIMENSIONS = ('data', 'baseline', 'evaluation', 'compute', 'timeline', 'compliance', 'pilot')
VALID = {'VERIFIED', 'NOT_REQUIRED', 'CONDITIONAL', 'BLOCKED', 'UNKNOWN'}


def assess_feasibility(card):
    """Fail closed on missing evidence, explicit blockers, and unbounded budgets."""
    if not isinstance(card, dict):
        return {'status': 'UNKNOWN', 'precheck_ready': False, 'issues': ['card must be object'],
                'disclaimer': 'Evidence fields are declarations, not independent validation.'}
    issues = []
    statuses = []
    for dim in DIMENSIONS:
        detail = card.get(dim)
        if not isinstance(detail, dict):
            issues.append(f'{dim}: missing structured evidence')
            statuses.append('UNKNOWN')
            continue
        status = detail.get('status', 'UNKNOWN')
        if status not in VALID:
            issues.append(f'{dim}: unsupported status')
            statuses.append('UNKNOWN')
            continue
        if status == 'VERIFIED' and not str(detail.get('evidence', '')).strip():
            issues.append(f'{dim}: VERIFIED requires specific evidence and where checked')
            status = 'UNKNOWN'
        if status == 'NOT_REQUIRED':
            if dim in ('baseline', 'evaluation', 'pilot', 'timeline', 'compliance'):
                issues.append(f'{dim}: must have an appropriate verification path, not NOT_REQUIRED')
                status = 'UNKNOWN'
            elif not str(detail.get('justification', '')).strip():
                issues.append(f'{dim}: NOT_REQUIRED needs discipline-specific justification')
                status = 'UNKNOWN'
        if status == 'CONDITIONAL' and not str(detail.get('resolution', '')).strip():
            issues.append(f'{dim}: CONDITIONAL needs concrete acquisition/mitigation path')
        if dim in ('compute', 'timeline') and detail.get('within_budget') is False:
            issues.append(f'{dim}: explicitly exceeds the available budget')
            status = 'BLOCKED'
        if dim == 'compliance' and detail.get('authorized') is False:
            issues.append('compliance: authorization absent')
            status = 'BLOCKED'
        statuses.append(status)
    if 'BLOCKED' in statuses:
        outcome = 'INFEASIBLE'
    elif 'UNKNOWN' in statuses:
        outcome = 'UNKNOWN'
    elif 'CONDITIONAL' in statuses:
        outcome = 'CONDITIONALLY_FEASIBLE'
    else:
        outcome = 'PRECHECK_EVIDENCE_PRESENT'
    return {'status': outcome, 'precheck_ready': outcome == 'PRECHECK_EVIDENCE_PRESENT',
            'issues': issues,
            'disclaimer': 'Offline presence/logic check only; FEASIBLE_VERIFIED requires human/tool verification of evidence, access, licenses, budget and pilot practicality.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    result = assess_feasibility(json.loads(Path(args.input).read_text(encoding='utf-8')))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        p = Path(args.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
    return 0 if result['precheck_ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
