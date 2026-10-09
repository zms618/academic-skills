import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.motivation_gate import assess
from scripts.workflow import main, STAGES
from tests.helpers import motivation_fixture, confirm_motivation_gate
from scripts.advisor_report_check import audit

class MotivationFirstTests(unittest.TestCase):
    def test_order_first_strong_problem_then_idea(self):
        self.assertLess(STAGES.index('MOTIVATION_GATE'),STAGES.index('DIVERGE'))
        self.assertLess(STAGES.index('MOTIVATION_GATE'),STAGES.index('DATA_SEARCH'))
        self.assertLess(STAGES.index('DATA_SEARCH'),STAGES.index('MOTIVATION_INITIAL'))
        self.assertLess(STAGES.index('MOTIVATION_INITIAL'),STAGES.index('MOTIVATION_RECHECK'))

    def test_unseen_shift_speculation_not_a_motivation(self):
        c=motivation_fixture()
        c['evidence']=[{'evidence_type':'HYPOTHESIZED', 'source':'unseen shift combinations could fail'}]
        r=assess(c)
        self.assertEqual('REJECT_OR_REFRAME',r['status'])
        self.assertFalse(r['can_generate_idea_seeds'])

    def test_one_benchmark_table_is_probe_only(self):
        c=motivation_fixture();c['evidence']=c['evidence'][:1]
        r=assess(c)
        self.assertEqual('PROBE_ONLY',r['status'])
        self.assertEqual('NO_NEW_MODEL_PROBLEM_PROBE',r['allowed_next_action'])
        self.assertFalse(r['ready'])

    def test_two_distinct_evidence_units_structural_pass_only(self):
        r=assess(motivation_fixture())
        self.assertEqual('PASS_FOR_IDEATION',r['status'])
        self.assertEqual(2,r['direct_evidence_units'])
        self.assertIn('NOT independently verified',r['limitations'])

    def test_two_claims_same_source_not_independent(self):
        c=motivation_fixture()
        c['evidence'][1]['independence_key']=c['evidence'][0]['independence_key']
        self.assertEqual('PROBE_ONLY',assess(c)['status'])

    def test_only_abstract_and_rhetoric_dont_pass(self):
        c=motivation_fixture()
        c['evidence']=[{'evidence_type':'ABSTRACT_ONLY', 'source':'paper title only'}]
        self.assertFalse(assess(c)['ready'])
        c=motivation_fixture();c['problem_importance']='提高鲁棒性'
        self.assertEqual('PROBE_ONLY',assess(c)['status'])

    def test_fair_control_explains_failure_stops(self):
        c=motivation_fixture();c['failure_disappears_under_fair_comparison']=True
        self.assertEqual('REJECT_OR_REFRAME',assess(c)['status'])

    def test_missing_source_access_requests_neutral_research(self):
        c=motivation_fixture();c['evidence']=[];c['source_access_blocked']=True
        self.assertEqual('RESEARCH_MORE',assess(c)['status'])

    def test_missing_alternatives_cannot_pass_even_with_two_tables(self):
        c=motivation_fixture();c['alternative_explanations']=[]
        self.assertEqual('PROBE_ONLY',assess(c)['status'])

    def test_no_direct_advance_without_m0_and_no_forged_ready(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            main(['init','--project',d]);
            for s in ('SEARCH','EXPLAIN','MOTIVATION_GATE'):
                main(['advance','--project',d,'--stage',s,'--reason','fixture'])
            def go(s): return main(['advance','--project',d,'--stage',s,'--reason','fixture'])
            with self.assertRaises(SystemExit):go('DIVERGE')
            (p/'motivation_gate_result.json').write_text('{"ready": true}',encoding='utf-8')
            with self.assertRaises(SystemExit):go('DIVERGE')
            self.assertEqual(0,confirm_motivation_gate(d))
            self.assertEqual(0,go('DIVERGE'))

    def test_editing_card_after_pass_invalidates_gate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);main(['init','--project',d])
            for s in ('SEARCH','EXPLAIN','MOTIVATION_GATE'):
                main(['advance','--project',d,'--stage',s,'--reason','fixture'])
            self.assertEqual(0,confirm_motivation_gate(d))
            f=p/'motivation_gate_card.json'
            c=json.loads(f.read_text(encoding='utf-8'));c['evidence']=[];f.write_text(json.dumps(c))
            with self.assertRaises(SystemExit):
                main(['advance','--project',d,'--stage','DIVERGE','--reason','edited source'])

    def test_failed_m0_report_forbids_premature_method(self):
        report={'protocol_version':'3.3','report_phase':'M0_PROBLEM_DISCOVERY',
                'status':'NEEDS_EVIDENCE','action':'RESEARCH_MORE',
                'motivation_gate':{'status':'PROBE_ONLY'},
                'problem_evidence_card':'Only one dataset figure; fairness not confirmed',
                'problem_importance':'Could explain unexpected DG failure',
                'alternative_explanations':['Unfair training budget','Different split'],
                'next_evidence_action':'Read original results then compare matching backbone and split'}
        self.assertEqual([],audit(report))
        report['potential_contributions']=[{'claim':'new graph'}]
        self.assertTrue(any('must not propose potential_contributions' in x for x in audit(report)))
        report['potential_contributions']=[]
        report['method_design']={'new_architecture':'router'}
        self.assertTrue(any('must not propose method_design' in x for x in audit(report)))

    def test_full_v33_report_cannot_omit_m0(self):
        from tests.test_advisor_v31 import good
        r=good();r['protocol_version']='3.3'
        self.assertTrue(any('requires M0' in x for x in audit(r)))
        r['motivation_gate']={'status':'PASS_FOR_IDEATION'}
        r['problem_evidence_card']='Source-located failures and confounds vetted by human reviewer'
        self.assertEqual([],audit(r))

if __name__=='__main__':unittest.main()
