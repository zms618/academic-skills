from tests.helpers import confirm_motivation_gate, confirm_dataset_sample
import json
import tempfile
import unittest
from pathlib import Path
from scripts.dataset_anchor import assess_anchor
from scripts.workflow import main,check_idea


def existing_fixture():
    return {
      'mode':'EXISTING',
      'dataset_name':'Fixture public dataset (NOT an actual source)',
      'source_url_or_local_path':'fixture://provided-dataset',
      'access_status':'DOWNLOADED_OR_OPENED',
      'access_evidence':'Fixture: checked accessible files (not real verification)',
      'license_or_permission_evidence':'Fixture: confirmed license text',
      'modalities_and_fields':'images and captions',
      'labels_or_supervision':'class label and caption',
      'evaluation_protocol':'heldout accuracy and robustness',
      'split_or_leakage_plan':'disjoint source and target splits',
      'baseline_path':'fixture://baseline-code',
      'dataset_fit_to_problem':'can simulate fixed corruptions and measure error',
      'requires_large_new_collection':False,
      'license_prohibits_use':False,
      'task_fields_available':True,
    }


class DatasetAnchorTests(unittest.TestCase):
    def test_existing_dataset_evidence_fields_present(self):
        self.assertTrue(assess_anchor(existing_fixture())['anchor_ready'])
    def test_only_webpage_mention_not_enough(self):
        a=existing_fixture();a['access_status']='NOT_TESTED'
        self.assertFalse(assess_anchor(a)['anchor_ready'])
    def test_no_new_data_collection(self):
        a=existing_fixture();a['requires_large_new_collection']=True
        self.assertFalse(assess_anchor(a)['anchor_ready'])
    def test_task_fields_must_be_present(self):
        a=existing_fixture();a['task_fields_available']=False
        self.assertFalse(assess_anchor(a)['anchor_ready'])
    def test_derived_requires_provenance(self):
        a=existing_fixture();a['mode']='DERIVED_FROM_EXISTING'
        self.assertFalse(assess_anchor(a)['anchor_ready'])
        a.update({'parent_dataset_name':'Source X','parent_dataset_source':'fixture://source',
                  'derivation_steps':'sample source frames then apply corruption with fixed seed',
                  'label_provenance':'same original class labels with validation','derived_dataset_cost':'one CPU hour',
                  'derived_split_protocol':'split original examples before transforms',
                  'parent_dataset_access_confirmed':True,'derivation_within_resources':True})
        self.assertTrue(assess_anchor(a)['anchor_ready'])
    def test_derived_not_within_budget(self):
        a=existing_fixture();a['mode']='DERIVED_FROM_EXISTING'
        a.update({'parent_dataset_name':'X','parent_dataset_source':'fixture://x','derivation_steps':'sample',
                  'label_provenance':'existing labels','derived_dataset_cost':'too high',
                  'derived_split_protocol':'source disjoint','parent_dataset_access_confirmed':True,
                  'derivation_within_resources':False})
        self.assertFalse(assess_anchor(a)['anchor_ready'])
    def test_dataset_change_invalidates_downstream_results(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            self.assertEqual(main(['init','--project',d]),0)
            for stage in ('SEARCH','EXPLAIN','MOTIVATION_GATE','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                if stage=='DIVERGE':self.assertEqual(confirm_motivation_gate(d),0)
                self.assertEqual(main(['advance','--project',d,'--stage',stage,'--reason','fixture']),0)
            first=p/'anchor1.json';first.write_text(json.dumps(existing_fixture()))
            self.assertEqual(main(['dataset-anchor','--project',d,'--card',str(first)]),0)
            self.assertEqual(confirm_dataset_sample(d),0)
            self.assertEqual(main(['advance','--project',d,'--stage','FEASIBILITY','--reason','first anchor']),0)
            (p/'feasibility_result.json').write_text(json.dumps({'precheck_ready':True}))
            altered=existing_fixture();altered['dataset_name']='Different verified fixture dataset'
            second=p/'anchor2.json';second.write_text(json.dumps(altered))
            self.assertEqual(main(['dataset-anchor','--project',d,'--card',str(second)]),0)
            self.assertEqual(confirm_dataset_sample(d),0)
            self.assertFalse((p/'feasibility_result.json').exists())
            self.assertEqual(json.loads((p/'workflow_state.json').read_text(encoding='utf-8'))['stage'],'DATA_ANCHOR')
    def test_audit_fails_if_dataset_anchor_missing(self):
        self.assertFalse(check_idea({'problem':'P','feasibility':{}})['gate_presence']['D0_existing_dataset_anchor'])
    def test_workflow_allows_idea_seed_but_blocks_feasibility_without_dataset(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            self.assertEqual(main(['init','--project',d]),0)
            self.assertEqual(main(['advance','--project',d,'--stage','SEARCH','--reason','fixture']),0)
            for stage in ('EXPLAIN','MOTIVATION_GATE','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                if stage=='DIVERGE':self.assertEqual(confirm_motivation_gate(d),0)
                self.assertEqual(main(['advance','--project',d,'--stage',stage,'--reason','idea first']),0)
            with self.assertRaises(SystemExit):
                main(['advance','--project',d,'--stage','FEASIBILITY','--reason','no data'])
            anchor=p/'anchor.json';anchor.write_text(json.dumps(existing_fixture()))
            self.assertEqual(main(['dataset-anchor','--project',d,'--card',str(anchor)]),0)
            self.assertEqual(confirm_dataset_sample(d),0)
            self.assertEqual(main(['advance','--project',d,'--stage','FEASIBILITY','--reason','check feasibility']),0)
            with self.assertRaises(SystemExit):
                main(['advance','--project',d,'--stage','FREEZE','--reason','no full feasibility'])

if __name__=='__main__': unittest.main()
