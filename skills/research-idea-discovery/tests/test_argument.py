from tests.helpers import confirm_motivation_gate, confirm_dataset_sample
import json
import tempfile
import unittest
from pathlib import Path
from scripts.argument_audit import audit_motivation, audit_story
from scripts.workflow import main,check_idea
from scripts.feasibility_check import DIMENSIONS
from tests.test_dataset_anchor import existing_fixture


def valid_feasibility():
    return {k:{'status':'VERIFIED','evidence':'fixture only, not genuine verification'} for k in DIMENSIONS}


def valid_motivation():
    return {
        'failure_observation':'Baseline fails on specified hard conditions',
        'failure_evidence':'A full paper with a failure plot',
        'scientific_stakes':'Genuine unexplained representation failure',
        'hidden_assumption':'Components are exchangeable across shifts',
        'competing_explanations':['A: data imbalance','B: unstable gradients'],
        'strong_baseline_limit':'Simple confidence filter cannot discriminate A from B',
        'why_now':'A newly available heldout benchmark gives an empirical test',
        'hypothesis':'Components differ in their vulnerability',
        'falsifier':'If component damage is uniform, the hypothesis is false',
        'unique_prediction':'Intervention A is more beneficial on selectively damaged components',
        'sources':[{'source':'fixture paper','locator':'Figure 2','evidence_level':'E3'}],
    }


def valid_story():
    a={k:k+' fixture text' for k in ('hook','status_quo','observed_gap','root_cause','central_insight',
         'mechanism','novelty_delta','discriminating_experiment','scope_and_limits','pitch_30s','intro_outline')}
    a['claim_evidence_map']=[{'claim':'Claim A','evidence_or_experiment':'Figure 2 or E0 planned','status':'PLANNED'}]
    a['review_rounds']=[{'round':r,'attack':'Strong objection to '+r,'response':'Argument responding to '+r,
                         'new_evidence_or_mechanism_delta':'New source or narrowed boundary '+r,'decision':'RESOLVED_WITH_EVIDENCE'} for r in ('M','N','R')]
    a['closest_prior_status']='PROVISIONALLY_DIFFERENTIATED'
    return a


class NarrativeTests(unittest.TestCase):
    def test_empty_motivation_fails(self):
        self.assertFalse(audit_motivation({})['ready'])
    def test_untraceable_abstract_not_evidence(self):
        a=valid_motivation();a['sources']=[{'source':'abstract','evidence_level':'E1'}]
        self.assertFalse(audit_motivation(a)['ready'])
    def test_need_two_competing_explanations(self):
        a=valid_motivation();a['competing_explanations']=['only one']
        self.assertFalse(audit_motivation(a)['ready'])
    def test_contradicted_motivation(self):
        a=valid_motivation();a['problem_status']='CONTRADICTED'
        self.assertEqual(audit_motivation(a)['status'],'MOTIVATION_REJECTED')
    def test_supported_motivation_fields(self):
        self.assertTrue(audit_motivation(valid_motivation())['ready'])
    def test_story_requires_three_different_reviews(self):
        a=valid_story();a['review_rounds']=a['review_rounds'][:1]
        self.assertFalse(audit_story(a)['ready'])
    def test_story_requires_claim_evidence(self):
        a=valid_story();a['claim_evidence_map']=[]
        self.assertFalse(audit_story(a)['ready'])
    def test_unresolved_collision_blocks(self):
        a=valid_story();a['closest_prior_status']='COLLISION_CONFIRMED'
        self.assertFalse(audit_story(a)['ready'])
    def test_complete_story_ready_for_human_review_only(self):
        a=audit_story(valid_story())
        self.assertTrue(a['ready'])
        self.assertEqual(a['status'],'STORY_STRUCTURE_READY_FOR_REVIEW')
        self.assertIn('not automatically proven',a['warning'])
    def test_idea_audit_demands_two_distinct_motivation_rounds(self):
        idea={'idea_id':'a','revision':1,'problem':'problem','hypothesis':'hypothesis',
              'falsifier':'falsifier','mechanism':'mechanism','unique_prediction':'prediction',
              'naive_baseline':'simple','closest_prior_work':[{'title':'fixture'}],
              'pilot':{'kill_signal':'stop'},'sources':[{'evidence_level':'E3'}],
              'feasibility':valid_feasibility(),'resources_checked':True}
        self.assertFalse(check_idea(idea)['gate_presence']['M1_initial_motivation'])
        self.assertFalse(check_idea(idea)['gate_presence']['M2_motivation_recheck'])
        idea['motivation_initial']=valid_motivation()
        self.assertTrue(check_idea(idea)['gate_presence']['M1_initial_motivation'])
        self.assertFalse(check_idea(idea)['gate_presence']['M2_motivation_recheck'])
        idea['story']=valid_story()
        self.assertTrue(check_idea(idea)['gate_presence']['S_story_review'])
        self.assertFalse(check_idea(idea)['gate_presence']['L_mechanism_logic'])
    def test_hard_gate_before_freeze_is_m1(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Path(folder)
            self.assertEqual(main(['init','--project',folder]),0)
            for stage in ('SEARCH','EXPLAIN','MOTIVATION_GATE','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                if stage=='DIVERGE':self.assertEqual(confirm_motivation_gate(folder),0)
                self.assertEqual(main(['advance','--project',folder,'--stage',stage,'--reason','fixture']),0)
            anchor=project/'anchor.json';anchor.write_text(json.dumps(existing_fixture()))
            self.assertEqual(main(['dataset-anchor','--project',folder,'--card',str(anchor)]),0)
            self.assertEqual(confirm_dataset_sample(folder),0)
            self.assertEqual(main(['advance','--project',folder,'--stage','FEASIBILITY','--reason','fixture']),0)
            feas=project/'feas.json';feas.write_text(json.dumps(valid_feasibility()))
            self.assertEqual(main(['feasibility','--project',folder,'--card',str(feas)]),0)
            self.assertEqual(main(['advance','--project',folder,'--stage','MOTIVATION_INITIAL','--reason','fixture']),0)
            with self.assertRaises(SystemExit):main(['advance','--project',folder,'--stage','FREEZE','--reason','no motivation'])
            mot=project/'mot.json';mot.write_text(json.dumps(valid_motivation()))
            self.assertEqual(main(['motivation-initial','--project',folder,'--card',str(mot)]),0)
            self.assertEqual(main(['advance','--project',folder,'--stage','FREEZE','--reason','fixture']),0)

if __name__=='__main__': unittest.main()
