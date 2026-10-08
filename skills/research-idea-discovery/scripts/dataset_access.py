#!/usr/bin/env python3
"""Verify bounded, *actual* local dataset sample access (not catalog/URL claims).

This makes no license/legal or whole-dataset reproducibility claims. A local
sample check is a narrow piece of evidence, not proof the full dataset exists.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

MAX_SAMPLE_BYTES = 2 * 1024 * 1024


def verify_sample(card):
    issues = []
    if not isinstance(card, dict):
        return {'status': 'NOT_VERIFIED', 'access_ready': False, 'issues': ['Expected object']}
    sample = Path(str(card.get('sample_file', ''))).expanduser()
    if not sample.is_file() or sample.is_symlink():
        return {'status': 'NOT_VERIFIED', 'access_ready': False,
                'issues': ['Actual readable regular local sample file required; URL/claim alone is insufficient']}
    size = sample.stat().st_size
    if size < 1 or size > MAX_SAMPLE_BYTES:
        return {'status': 'NOT_VERIFIED', 'access_ready': False,
                'issues': ['Sample must be 1 byte to 2 MiB; use a small, lawful excerpt']}
    data = sample.read_bytes()
    if data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
        issues.append('HTML landing page is not a dataset sample')
    required = card.get('required_fields')
    if not isinstance(required, list) or not required or not all(isinstance(x, str) and x.strip() for x in required):
        issues.append('List exact required_fields/labels before verification')
        required = []
    observed = []
    try:
        if sample.suffix.lower() == '.csv':
            with sample.open(encoding='utf-8-sig', newline='') as f:
                observed = next(csv.reader(f), [])
                if next(csv.reader(f), None) is None:
                    issues.append('CSV needs a header and at least one example row')
        elif sample.suffix.lower() in ('.json', '.jsonl'):
            content = sample.read_text(encoding='utf-8')
            obj = json.loads(content.splitlines()[0]) if sample.suffix.lower() == '.jsonl' else json.loads(content)
            row = obj[0] if isinstance(obj, list) and obj else obj
            if not isinstance(row, dict):
                issues.append('JSON sample needs a row object with named fields')
            else:
                observed = list(row)
        else:
            issues.append('Only CSV/JSON/JSONL samples permit field-level validation in this tool')
    except (UnicodeError, ValueError, OSError) as exc:
        issues.append('Could not parse sample: ' + str(exc)[:160])
    missing = sorted(set(required) - set(observed))
    if missing:
        issues.append('Required fields missing from actual sample: ' + ', '.join(missing))
    license_path = Path(str(card.get('license_file', ''))).expanduser()
    license_source_present = license_path.is_file() and not license_path.is_symlink() and 0 < license_path.stat().st_size < 1024 * 1024
    if not license_source_present:
        issues.append('Local license/terms reference not supplied; legal use unverified')
    source_url = str(card.get('source_url', ''))
    parsed=urlparse(source_url)
    host=(parsed.hostname or '').lower()
    if parsed.scheme!='https' or not host or host.endswith(('.invalid','.test','.localhost')) or host in ('example.com','example.org','example.net'):
        issues.append('Plausible HTTPS official source URL required; placeholder/invalid hosts rejected')
    ready = not issues
    return {
        'status': 'LOCAL_SAMPLE_CHECKED_REQUIRES_HUMAN_SOURCE_REVIEW' if ready else 'NOT_VERIFIED',
        'access_ready': ready,
        'sample_access_verified': not any('sample' in issue.lower() or 'HTML' in issue for issue in issues),
        'required_fields_confirmed': bool(observed) and not missing,
        'license_source_present': license_source_present,
        'source_url': card.get('source_url'), 'observed_fields': observed,
        'sample_sha256': hashlib.sha256(data).hexdigest(), 'sample_bytes': size,
        'issues': issues,
        'limitations': 'Proof only that provided local bytes contain listed fields. Neither full dataset nor origin, license grant, split integrity, or reproducibility are independently certified.'
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args(argv)
    result = verify_sample(json.loads(Path(args.manifest).read_text(encoding='utf-8')))
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(result['status'])
    return 0 if result['access_ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())