from tests.helpers import confirm_dataset_sample
import json
import tempfile
import unittest
from pathlib import Path
from scripts.feasibility_check import assess_feasibility, DIMENSIONS
from scripts.workflow import check_idea, main
from tests.test_dataset_anchor import existing_fixture


def valid_card():
    return {k: {'status':'VERIFIED','evidence': f'Example only: checked {k} evidence (must independently verify)'} for k in DIMENSIONS}


class FeasibilityTests(unittest.TestCase):
    def test_no_dataset_no_route_is_not_ready(self):
        card=valid_card();card['data']={'status':'BLOCKED','reason':'No permitted data'}
        r=assess_feasibility(card)
        self.assertEqual(r['status'],'INFEASIBLE')
        self.assertFalse(r['precheck_ready'])

    def test_unknown_is_not_feasible(self):
        card=valid_card();card['data']={'status':'UNKNOWN'}
        self.assertEqual(assess_feasibility(card)['status'],'UNKNOWN')

    def test_conditional_cannot_proceed(self):
        card=valid_card();card['data']={'status':'CONDITIONAL','resolution':'Get agreement'}
        self.assertEqual(assess_feasibility(card)['status'],'CONDITIONALLY_FEASIBLE')

    def test_missing_evidence_fails_closed(self):
        card=valid_card();card['data']={'status':'VERIFIED'}
        self.assertFalse(assess_feasibility(card)['precheck_ready'])

    def test_budget_overrun_blocks(self):
        card=valid_card();card['compute']['within_budget']=False
        self.assertEqual(assess_feasibility(card)['status'],'INFEASIBLE')

    def test_theory_no_dataset_with_justification(self):
        card=valid_card();card['data']={'status':'NOT_REQUIRED','justification':'Theorem and counterexample only'}
        self.assertTrue(assess_feasibility(card)['precheck_ready'])

    def test_syntactic_precheck_not_real_world_validation(self):
        card=valid_card();r=assess_feasibility(card)
        self.assertEqual(r['status'],'PRECHECK_EVIDENCE_PRESENT')
        self.assertIn('requires human/tool verification',r['disclaimer'])

    def test_idea_gate_requires_feasibility_card(self):
        minimal={'idea_id':'X','revision':1,'problem':'P','hypothesis':'H','falsifier':'F','mechanism':'M',
                 'unique_prediction':'UP','naive_baseline':'NB','closest_prior_work':[{'title':'X'}],
                 'pilot':{'kill_signal':'stop'},'sources':[{'evidence_level':'E3'}],
                 'novelty_verdict':'PROVISIONALLY_DIFFERENTIATED','resources_checked':True}
        self.assertFalse(check_idea(minimal)['gate_presence']['G0_feasibility'])
        minimal['feasibility']=valid_card()
        self.assertTrue(check_idea(minimal)['gate_presence']['G0_feasibility'])

    def test_workflow_fails_closed_before_feasibility_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            self.assertEqual(main(['init','--project',d]),0)
            self.assertEqual(main(['advance','--project',d,'--stage','SEARCH','--reason','search done']),0)
            for stage in ('EXPLAIN','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                self.assertEqual(main(['advance','--project',d,'--stage',stage,'--reason','idea first']),0)
            with self.assertRaises(SystemExit):
                main(['advance','--project',d,'--stage','FEASIBILITY','--reason','no verified data yet'])
            anchor=p/'anchor.json';anchor.write_text(json.dumps(existing_fixture()))
            self.assertEqual(main(['dataset-anchor','--project',d,'--card',str(anchor)]),0)
            self.assertEqual(confirm_dataset_sample(d),0)
            self.assertEqual(main(['advance','--project',d,'--stage','FEASIBILITY','--reason','evaluate candidate']),0)
            card=p/'feas.json';card.write_text(json.dumps(valid_card()))
            self.assertEqual(main(['feasibility','--project',d,'--card',str(card)]),0)
            self.assertEqual(main(['advance','--project',d,'--stage','MOTIVATION_INITIAL','--reason','precheck exists']),0)


if __name__=='__main__': unittest.main()
