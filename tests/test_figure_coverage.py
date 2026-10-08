import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/paper-reading/scripts/check_figure_coverage.py'
SPEC = importlib.util.spec_from_file_location('check_figure_coverage', SCRIPT)
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


def _asset(asset_id, visual_type='architecture', stages=None):
    stages = stages or [1]
    return {
        'id': asset_id,
        'kind': 'figure',
        'visual_type': visual_type,
        'pdf_page': 1,
        'caption': 'Verified caption',
        'visually_observed': 'Observed original figure content',
        'body_reference': 'Introduction, paragraph 2',
        'argument_role': 'Shows the motivating failure',
        'why_required': 'Needed to explain the problem',
        'required_stages': stages,
        'first_stage': min(stages),
        'revisit_stages': [],
    }


def test_audit_accepts_complete_stage_records():
    plan = {
        'assets': [_asset('fig1')],
        'stage_audit': {'1': {'fig1': {'display_attempted': True, 'explained': True}}},
        'required_links': [],
    }
    assert coverage.audit_plan(plan, 1) == []


def test_audit_requires_every_essential_visual_in_stage():
    plan = {
        'assets': [_asset('fig1'), _asset('fig2', visual_type='result')],
        'stage_audit': {'1': {'fig1': {'display_attempted': True, 'explained': True}}},
        'required_links': [],
    }
    errors = coverage.audit_plan(plan, 1)
    assert any('fig2' in error and 'not both displayed/attempted and explained' in error for error in errors)


def test_audit_does_not_accept_truthy_strings_as_completed_checks():
    plan = {
        'assets': [_asset('fig1')],
        'stage_audit': {'1': {'fig1': {'display_attempted': 'false', 'explained': 'false'}}},
        'required_links': [],
    }
    assert any('not both displayed/attempted and explained' in error for error in coverage.audit_plan(plan, 1))


def test_stage_two_requires_a_verified_method_visual_classification():
    plan = {
        'assets': [_asset('fig2', stages=[2])],
        'stage_audit': {'2': {'fig2': {'display_attempted': True, 'explained': True}}},
        'required_links': [],
        'method_overview': {
            'type': 'architecture',
            'explicitly_declared': True,
            'input_output_explained': True,
            'intuitive_flow_explained': True,
        },
    }
    assert coverage.audit_plan(plan, 2) == []
    plan['method_overview']['type'] = 'pipeline_only'
    errors = coverage.audit_plan(plan, 2)
    assert any('must state no separate network architecture diagram' in error for error in errors)


def test_audit_reports_malformed_plan_instead_of_crashing():
    assert coverage.audit_plan([], 1) == ['plan must be a JSON object']
    plan = {'assets': ['not-an-object'], 'stage_audit': [], 'required_links': 'invalid'}
    errors = coverage.audit_plan(plan, 1)
    assert 'asset 0: must be an object' in errors
    assert 'stage_audit must be an object' in errors
    assert 'required_links must be a list' in errors
