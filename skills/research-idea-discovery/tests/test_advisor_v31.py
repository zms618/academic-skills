import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('advisor_report_check',ROOT/'scripts/advisor_report_check.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def good():
    return {'status':'PROMISING_SEED','action':'GO_E0','plain_language_question':'模态失效后是否应该继续适应？',
        'concrete_example':'toy samples, A/B','motivation':'real task and scientific question',
        'prior_work':'nearest methods assessed','hypothesis':'falsifiable',
        'potential_contributions':[{'claim':'new prediction','status':'EVIDENCE_PENDING','required_evidence':'diagnostic figure','nearest_prior':'PASLE candidate-label TTA','novelty_delta':'class-pair proxy tested beyond sample confidence','distinguishing_test':'stratified update harm prediction versus entropy','necessity_ablation':'replace pair proxy with sample confidence','kill_signal':'no residual effect'}],
        'scientific_story':'Observation -> Failure -> Hypothesis -> Mechanism -> Evidence',
        'feasibility':{'dataset':'dataset official page, access pending','model_checkpoint':'checkpoint inspected only','baselines':'Source, freeze, strong prior','data_access_status':'ACCESS_PENDING','evaluation_protocol':'matched split and metric'},
        'first_48h':['inspect availability, labels, checkpoint','run tiny Source and freeze E0'],
        'first_week':'days 1 to 7 with artifacts', 'kill_criteria':['no target failure','simple rival same'],
        'reviewer_risks':'closest-neighbor and simple baseline','teach_back':'一句人话',
        'pilot_status':'PLANNED',
        'method_status':'DESIGN_PROPOSED',
        'method_design':{'track':'DL','task_io':'audio video to event classes','baseline_decision':'source uses fused logits',
          'decision_rule':'mask high evidence pairs only','implementation_limitations':'test labels absent; cannot recreate missing signal',
          'weakest_assumption':'pair proxy predicts harmful adaptation beyond confidence','cost_scaling':'O(C^2) per sample without sparse pair selection',
          'estimator':{'observables':'source priors and feature perturbation stability','formula_or_procedure':'stable margins / calibrated prior', 'validation_test':'predict errors conditioned on entropy'},
          'loss_or_algorithm':'masked teacher margin and source magnitude guard', 'frozen_parameters':'encoders',
          'updated_parameters':'small fusion adapter','integration':{'repo_url_or_status':'https://github.com/he4cs/DASP','entrypoint_status':'TO_LOCATE','first_function':'pair_evidence', 'input_contract':'modality embedding tensor', 'output_contract':'pairwise score'},
          'update_timeline':['t0: compute source snapshot then choose update','t1: recompute proxy and update new batch'],
          'test_label_policy':'NO_LABELS_ONLINE','source_data_policy':'source prototypes stored offline only if allowed','shift_protocol':'corruption and missingness are separate settings','leakage_controls':'no target labels for model updates or threshold selection'},
        'researcher_trial':{'student_blockers':'exact checkpoint mapping unknown','reviewer_attacks':'simpler skip update','fixes_applied':'add no-update control','remaining_unknowns':'whether target evidence is observable','simulation_status':'ROLE_SIMULATED'},
        'action_cards':[{'prerequisite':'repo access','action':'inspect configs','artifact':'inventory.csv','interpretation':'checkpoint mapping confirmed or blocked'},
                        {'prerequisite':'labels offline','action':'source inference','artifact':'source.csv','interpretation':'corruption effect measured'},
                        {'prerequisite':'source csv','action':'compare adapted vs no update','artifact':'harm.csv','interpretation':'GO or STOP'}]}

class AdvisorV31Test(unittest.TestCase):
    def test_usable_candidate_passes_structure(self):self.assertEqual([],mod.audit(good()))
    def test_missing_explanation_fails(self):
        x=good();x.pop('concrete_example');self.assertIn('missing concrete_example',mod.audit(x))
    def test_no_dataset_model_fails(self):
        x=good();x['feasibility'].pop('dataset');x['feasibility'].pop('model_checkpoint');self.assertTrue(any('feasibility missing' in i for i in mod.audit(x)))
    def test_three_contributions_not_mandatory(self):self.assertEqual([],mod.audit(good()))
    def test_four_contributions_rejected(self):
        x=good();x['potential_contributions'] *= 4;self.assertTrue(any('at most three' in i for i in mod.audit(x)))
    def test_unsubstantiated_validated_claim(self):
        x=good();x['potential_contributions'][0]['status']='VALIDATED';self.assertTrue(any('VALIDATED' in i for i in mod.audit(x)))
    def test_dangerously_strong_verdict(self):
        x=good();x['status']='STRONG_CANDIDATE';self.assertTrue(any('STRONG_CANDIDATE incompatible' in i for i in mod.audit(x)))
    def test_no_idea_needs_deep_research_prompt(self):
        x={'status':'NO_DEFENSIBLE_IDEA_FOUND','action':'RESEARCH_MORE','rejected_reasons':'prior art collisions','missing_evidence':'full papers','next_evidence_action':'search latest'}
        self.assertTrue(any('Deep Research' in i for i in mod.audit(x)))
        x['deep_research_prompt']='Search specific similar scientific mechanisms.';self.assertEqual([],mod.audit(x))
    def test_fake_pilot_executed(self):
        x=good();x['pilot_status']='EXECUTED';self.assertIn('executed pilot requires log reference',mod.audit(x))
    def test_main_skill_links_protocols(self):
        t=(ROOT/'skills/research-idea-discovery/SKILL.md').read_text(encoding='utf-8')
        for s in ('plain-language-idea-protocol.md','research-execution-protocol.md','scientific-story-and-contributions.md','research-advisor-output-protocol.md'):
            self.assertIn(s,t)
    def test_manifest_defaults_retained(self):
        m=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
        l=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual('3.5.0',m['version']);self.assertEqual(m['version'],l['version'])
        self.assertEqual(3,len(m['extensions']['com.openai']['interface']['defaultPrompt']))
        self.assertEqual(m['extensions']['com.openai']['interface']['defaultPrompt'],l['interface']['defaultPrompt'])

if __name__=='__main__':unittest.main()
