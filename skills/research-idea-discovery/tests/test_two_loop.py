from tests.helpers import confirm_motivation_gate, confirm_dataset_sample, confirm_literature_coverage
import json
import tempfile
import unittest
from pathlib import Path
from scripts.workflow import main,STAGES
from scripts.argument_audit import audit_logic,audit_motivation_recheck,audit_novelty
from tests.test_argument import valid_feasibility,valid_motivation,valid_story
from tests.test_dataset_anchor import existing_fixture

def valid_novelty(idea='x',rev=1):
    return {'idea_id':idea,'revision':rev,'novelty_verdict':'PROVISIONALLY_DIFFERENTIATED',
        'novelty_delta':'Different causal dependency with an independent prediction',
        'unique_prediction':'Extra benefit only on selectively degraded samples',
        'closest_prior_work':[{'title':'Strong neighbor','source':'fixture://paper',
          'method_locator':'section 3','mechanism':'existing selective modality adaptation',
          'overlap':'both choose features','difference':'region-specific causal decision',
          'evidence_level':'E3'}]}

def valid_logic(idea='x',rev=1):
    return {'idea_id':idea,'revision':rev,'problem_cause':'region specific damage',
        'intervention':'fine grained evidence selection',
        'causal_bridge':'preserve intact regions while changing damaged features',
        'strongest_prior_mechanism':'global reliability weighting',
        'simple_rival':'fixed confidence threshold',
        'rival_distinction':'calibrated matched confidence intervention',
        'necessity_ablation':'turn off localized decision and match FLOPs',
        'unique_prediction':'localized heterogeneity matters',
        'discriminating_test':'selective shift vs global shift on same labels',
        'confounders':['class imbalance','shift severity'],
        'failure_boundary':'uniform shifts should favor simpler baseline'}

def valid_recheck(idea='x',rev=1):
    return {'idea_id':idea,'revision':rev,
        'original_problem_claim':'all multimodal TTA overlooks differences',
        'closest_prior_work':'Strong neighbor, section 3',
        'prior_work_explains':'modality-level differences are already adapted',
        'remaining_gap':'specific within-modality heterogeneous corruption remains untested',
        'importance_after_prior_art':'local failures degrade prediction in critical regions',
        'revised_central_claim':'assess whether local failures require local decisions',
        'distinctive_prediction':'gains isolated on locally heterogeneous corruptions',
        'new_falsifier':'fixed confidence filter works equally well',
        'revision_rationale':'narrowed claim after reading strong baseline',
        'novelty_status':'PROVISIONALLY_DIFFERENTIATED',
        'sources':[{'source':'fixture neighbor','locator':'sec 3','evidence_level':'E3'}]}

class TwoLoopTests(unittest.TestCase):
    def test_unresolved_review_cannot_pass_story_gate(self):
        from scripts.argument_audit import audit_story
        s=valid_story()
        s['review_rounds'][0]['decision']='REVISE'
        self.assertFalse(audit_story(s)['ready'])
    def test_partially_unverified_novelty_never_automatically_ready(self):
        s=valid_novelty();s['novelty_verdict']='DISTINCT_BUT_UNVERIFIED'
        self.assertFalse(audit_novelty(s)['ready'])
    def test_stage_order(self):
        s=STAGES
        self.assertLess(s.index('MOTIVATION_INITIAL'),s.index('SCOOP'))
        self.assertLess(s.index('SCOOP'),s.index('MECHANISM_LOGIC'))
        self.assertLess(s.index('MECHANISM_LOGIC'),s.index('MOTIVATION_RECHECK'))
        self.assertLess(s.index('MOTIVATION_RECHECK'),s.index('NARRATIVE'))
    def test_fails_missing_logic_or_post_novelty_motivation(self):
        self.assertFalse(audit_logic({})['ready'])
        self.assertFalse(audit_motivation_recheck({})['ready'])
        a=valid_logic();a['simple_rival_outcome']='EQUIVALENT_OR_BETTER'
        self.assertFalse(audit_logic(a)['ready'])
        a=valid_recheck();a['gap_status']='COVERED'
        self.assertFalse(audit_motivation_recheck(a)['ready'])
    def test_fails_unverified_close_prior(self):
        a=valid_novelty();a['closest_prior_work'][0]['evidence_level']='E1'
        self.assertFalse(audit_novelty(a)['ready'])
    def test_full_loop_and_changed_input_invalidates_old_logic_and_story(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            def run(*args): return main(list(args)+['--project',d])
            def card(name,record):
                f=p/(name+'.json');f.write_text(json.dumps(record,ensure_ascii=False));return str(f)
            def go(stage):return main(['advance','--project',d,'--stage',stage,'--reason','fixture'])
            self.assertEqual(run('init'),0)
            for stage in ('SEARCH','EXPLAIN','MOTIVATION_GATE','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                if stage=='DIVERGE':self.assertEqual(confirm_motivation_gate(d),0)
                go(stage)
            self.assertEqual(main(['dataset-anchor','--project',d,'--card',card('anchor',existing_fixture())]),0)
            self.assertEqual(confirm_dataset_sample(d),0)
            go('FEASIBILITY')
            self.assertEqual(main(['feasibility','--project',d,'--card',card('feasibility',valid_feasibility())]),0)
            go('MOTIVATION_INITIAL')
            with self.assertRaises(SystemExit):go('FREEZE')
            self.assertEqual(main(['motivation-initial','--project',d,'--card',card('m1',valid_motivation())]),0)
            go('FREEZE');go('SCOOP')
            with self.assertRaises(SystemExit):go('MECHANISM_LOGIC')
            self.assertEqual(main(['novelty','--project',d,'--card',card('nov',valid_novelty())]),0)
            self.assertEqual(confirm_literature_coverage(d),0)
            go('MECHANISM_LOGIC')
            with self.assertRaises(SystemExit):go('MOTIVATION_RECHECK')
            # Cannot mix audits for different proposals.
            with self.assertRaises(SystemExit): main(['logic','--project',d,'--card',card('wrong-logic',valid_logic('another'))])
            self.assertEqual(main(['logic','--project',d,'--card',card('logic',valid_logic())]),0)
            go('MOTIVATION_RECHECK')
            with self.assertRaises(SystemExit):go('NARRATIVE')
            self.assertEqual(main(['motivation-recheck','--project',d,'--card',card('m2',valid_recheck())]),0)
            go('NARRATIVE')
            with self.assertRaises(SystemExit):go('REVIEW')
            self.assertEqual(main(['narrative','--project',d,'--card',card('story',valid_story())]),0)
            go('REVIEW')
            # Explicitly go back to revise; downstream outputs become stale.
            self.assertEqual(main(['advance','--project',d,'--stage','SCOOP','--reason','closest paper found']),0)
            self.assertFalse((p/'logic_result.json').exists())
            self.assertFalse((p/'motivation_recheck_result.json').exists())
            self.assertFalse((p/'narrative_result.json').exists())
    def test_recheck_must_not_copy_original_without_new_neighbor_comparison(self):
        a=valid_recheck();a['revision_rationale']='unchanged'
        self.assertFalse(audit_motivation_recheck(a)['ready'])
    def test_legacy_motivation_stage_invalidated(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); main(['init','--project',d]);data=json.loads((p/'workflow_state.json').read_text(encoding='utf-8'))
            data['stage']='MOTIVATION';(p/'workflow_state.json').write_text(json.dumps(data))
            main(['status','--project',d]);self.assertEqual(json.loads((p/'workflow_state.json').read_text(encoding='utf-8'))['stage'],'FEASIBILITY')

if __name__=='__main__':unittest.main()
