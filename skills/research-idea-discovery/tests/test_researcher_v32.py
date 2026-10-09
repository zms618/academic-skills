import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('advisor_check32',ROOT/'scripts/advisor_report_check.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

from test_advisor_v31 import good

class ResearcherValue32(unittest.TestCase):
    def test_full_method_is_required(self):
        x=good();x.pop('method_design');self.assertTrue(any('method_design' in i for i in mod.audit(x)))
    def test_empty_estimator_rejected(self):
        x=good();x['method_design']['estimator']={};self.assertTrue(any('estimator' in i for i in mod.audit(x)))
    def test_implementation_interface_required(self):
        x=good();x['method_design']['integration'].pop('first_function');self.assertTrue(any('integration' in i for i in mod.audit(x)))
    def test_only_one_contribution_is_ok(self):self.assertEqual([],mod.audit(good()))
    def test_no_independent_prediction_rejected(self):
        x=good();x['potential_contributions'][0].pop('distinguishing_test',None);self.assertTrue(any('contribution' in i for i in mod.audit(x)))
    def test_v3_1_weak_candidate_has_no_executable_method(self):
        x=good();x.pop('method_design');x.pop('method_status');x.pop('researcher_trial');x.pop('action_cards');self.assertGreaterEqual(len(mod.audit(x)),4)
    def test_fake_implementation_status_rejected(self):
        x=good();x['method_status']='IMPLEMENTATION_VERIFIED';self.assertTrue(any('implementation_test_log' in i for i in mod.audit(x)))
    def test_fake_executed_status_rejected(self):
        x=good();x['method_status']='EXECUTED_WITH_LOGS';self.assertTrue(any('pilot_metrics_reference' in i for i in mod.audit(x)))
    def test_strong_with_method_not_ready_rejected(self):
        x=good();x['method_status']='METHOD_NOT_READY';x['status']='STRONG_CANDIDATE';x['feasibility']['data_access_status']='LOCAL_SAMPLE_CHECKED';self.assertTrue(any('METHOD_NOT_READY' in i for i in mod.audit(x)))
    def test_non_ml_plan_works(self):
        x=good();x['method_design']={'track':'NON_DL','task_io':'sample to physical test','baseline_decision':'old physical model',
          'decision_rule':'measurement condition A vs B', 'weakest_assumption':'material classes differ',
          'cost_scaling':'N replicates','implementation_limitations':'limited equipment',
          'operational_protocol':'prepare controlled material samples','controls':'same preparation batch','falsifying_observation':'no replicated shift'}
        self.assertEqual([],mod.audit(x))
    def test_no_defensible_idea_route_still_allowed(self):
        x={'status':'NO_DEFENSIBLE_IDEA_FOUND','action':'RESEARCH_MORE','rejected_reasons':'same as closest mechanism',
          'missing_evidence':'dataset inaccessible','next_evidence_action':'inspect official dataset',
          'deep_research_prompt':'Investigate concrete existing research papers and existing public datasets'}
        self.assertEqual([],mod.audit(x))
    def test_duplicate_contributions_rejected(self):
        x=good();x['potential_contributions'] *= 2
        self.assertTrue(any('reuse identical' in i for i in mod.audit(x)))
    def test_placeholder_mechanism_rejected(self):
        x=good();x['method_design']['decision_rule']='提高鲁棒性'
        self.assertTrue(any('empty jargon' in i for i in mod.audit(x)))
    def test_source_data_leakage_field_required(self):
        x=good();x['method_design'].pop('source_data_policy')
        self.assertTrue(any('source_data_policy' in i for i in mod.audit(x)))
    def test_missingness_protocol_required(self):
        x=good();x['method_design'].pop('shift_protocol')
        self.assertTrue(any('shift_protocol' in i for i in mod.audit(x)))
    def test_materials_require_no_gpu_or_neural_loss(self):
        t=(ROOT/'skills/research-idea-discovery/references/researcher-value-acceptance.md').read_text(encoding='utf-8')
        self.assertIn('Non-DL or theory',t)
    def test_v32_method_designer_linked_to_main(self):
        t=(ROOT/'skills/research-idea-discovery/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('method-design-and-necessity.md',t)
        self.assertIn('researcher-value-acceptance.md',t)
        self.assertTrue((ROOT/'skills/research-method-designer/SKILL.md').is_file())

if __name__=='__main__':unittest.main()
