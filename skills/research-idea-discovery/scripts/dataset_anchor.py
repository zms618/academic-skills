#!/usr/bin/env python3
"""Offline D0 existing-dataset anchor precheck.

This audits the evidence FIELDS supplied by a researcher. It does NOT independently
visit dataset URLs, prove that a download works, or approve licenses.
"""
import argparse
import json
from pathlib import Path

ACCESS_STATES = {'DOWNLOADED_OR_OPENED', 'ACCESS_GRANT_CONFIRMED'}
DATASET_MODES = {'EXISTING', 'DERIVED_FROM_EXISTING'}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def assess_anchor(card):
    problems = []
    if not isinstance(card, dict):
        return {'status': 'DATASET_NOT_VERIFIED', 'anchor_ready': False,
                'issues': ['dataset_anchor must be an object'],
                'disclaimer': 'Offline metadata and declaration check, NOT independent access/license verification.'}
    mode = card.get('mode')
    if mode not in DATASET_MODES:
        problems.append('mode must be EXISTING or DERIVED_FROM_EXISTING; from-scratch collection is not allowed')
    for field in ('dataset_name', 'source_url_or_local_path', 'access_evidence',
                  'license_or_permission_evidence', 'modalities_and_fields',
                  'labels_or_supervision', 'evaluation_protocol', 'split_or_leakage_plan',
                  'baseline_path', 'dataset_fit_to_problem'):
        if not _text(card.get(field)):
            problems.append(f'{field} must contain specific, checkable information')
    if card.get('access_status') not in ACCESS_STATES:
        problems.append('access_status must show actual access or a confirmed authorization; landing-page mention is insufficient')
    if card.get('requires_large_new_collection') is not False:
        problems.append('large-scale from-scratch collection or annotation is outside the user resource constraint')
    if card.get('license_prohibits_use') is not False:
        problems.append('dataset license/use permission must not prohibit the intended study')
    if card.get('task_fields_available') is not True:
        problems.append('required data/labels/fields must be available for the testable task')
    if mode == 'DERIVED_FROM_EXISTING':
        for field in ('parent_dataset_name', 'parent_dataset_source', 'derivation_steps',
                      'label_provenance', 'derived_dataset_cost', 'derived_split_protocol'):
            if not _text(card.get(field)):
                problems.append(f'derived dataset requires {field}')
        if card.get('parent_dataset_access_confirmed') is not True:
            problems.append('parent dataset access must be confirmed before a derived dataset can qualify')
        if card.get('derivation_within_resources') is not True:
            problems.append('derivation must fit existing resources without large new collection/annotation')
    return {'status': 'EVIDENCE_FIELDS_PRESENT' if not problems else 'DATASET_NOT_VERIFIED',
            'anchor_ready': not problems, 'issues': problems,
            'disclaimer': 'Offline structural precheck only. Model/researcher must verify actual URL/local access, terms, labels, splits and task fit before claiming data readiness.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True)
    ap.add_argument('--output')
    a = ap.parse_args()
    result = assess_anchor(json.loads(Path(a.input).read_text(encoding='utf-8')))
    out = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.output:
        p = Path(a.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(out, encoding='utf-8')
    print(out, end='')
    return 0 if result['anchor_ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
