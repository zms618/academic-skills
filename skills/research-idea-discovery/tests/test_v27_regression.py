import json
import tempfile
import unittest
from pathlib import Path
from scripts.dataset_access import verify_sample
from scripts.execution_evidence import pilot_record, review_record
from scripts.literature_coverage import report
from scripts.idea_ledger import add
from scripts.pilot_bridge import run as run_pilot
from scripts.workflow import main
from tests.helpers import confirm_dataset_sample
import sys


class V27RegressionTests(unittest.TestCase):
    def sample(self,p):
        p=Path(p)
        (p/'sample.csv').write_text('visual,label\nimage.png,car\n',encoding='utf-8')
        (p/'license.txt').write_text('License text needs human source review',encoding='utf-8')
        return {'sample_file':str(p/'sample.csv'),'license_file':str(p/'license.txt'),
                'required_fields':['visual','label'], 'source_url':'https://huggingface.co/datasets/research-lab/test'}

    def test_invalid_link_without_sample_rejected(self):
        r=verify_sample({'source_url':'https://example.invalid/nonexistent.zip',
                         'sample_file':'/nonexistent','required_fields':['x']})
        self.assertFalse(r['access_ready'])
    def test_fake_invalid_url_even_with_local_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            card=self.sample(p);card['source_url']='https://example.invalid/bogus';
            self.assertFalse(verify_sample(card)['access_ready'])
    def test_local_sample_is_not_full_dataset_claim(self):
        with tempfile.TemporaryDirectory() as p:
            result=verify_sample(self.sample(p))
            self.assertTrue(result['access_ready']);self.assertIn('only',result['limitations'].lower())
            self.assertNotIn('FULL_DATASET_VERIFIED',result['status'])
    def test_sample_missing_label_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            card=self.sample(p);card['required_fields']=['visual','label','target_mask']
            self.assertFalse(verify_sample(card)['access_ready'])
    def test_html_page_as_dataset_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            card=self.sample(p);Path(card['sample_file']).write_text('<html>download</html>')
            self.assertFalse(verify_sample(card)['access_ready'])
    def test_forged_ready_file_does_not_bypass_dataset_gate(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);main(['init','--project',p]);
            for stage in ('SEARCH','EXPLAIN','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                main(['advance','--project',p,'--stage',stage,'--reason','test'])
            (root/'dataset_access_result.json').write_text('{"access_ready":true}')
            with self.assertRaises(SystemExit):main(['advance','--project',p,'--stage','FEASIBILITY','--reason','forged'])
    def test_review_stage_requires_specific_record_and_idea_revision(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);main(['init','--project',p]);state=json.loads((root/'workflow_state.json').read_text());state['stage']='REVIEW';
            (root/'workflow_state.json').write_text(json.dumps(state))
            with self.assertRaises(SystemExit):main(['advance','--project',p,'--stage','PILOT','--reason','no review'])
            (root/'review_result.json').write_text('{"ready":true}')
            with self.assertRaises(SystemExit):main(['advance','--project',p,'--stage','PILOT','--reason','fake ready'])
            card={'idea_id':'A','revision':1,'verdict':'PROCEED_TO_PILOT','critical_objections_unresolved':False,
                  'objections':[{'concern':'weak motivation','evidence_or_response':'test'},
                                {'concern':'same as prior','evidence_or_response':'test'}]}
            src=root/'card.json';src.write_text(json.dumps(card))
            (root/'novelty_result.json').write_text(json.dumps({'idea_id':'A','revision':1}))
            self.assertEqual(main(['record-review','--project',p,'--card',str(src)]),0)
            self.assertEqual(main(['advance','--project',p,'--stage','PILOT','--reason','documented review']),0)
    def test_review_revision_rejected(self):
        self.assertFalse(review_record({'verdict':'PROCEED_TO_PILOT','critical_objections_unresolved':True})['ready'])
    def test_dry_run_not_successful_pilot(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);run_pilot([sys.executable,'-c','print(123)'],root,root/'logs',execute=False)
            self.assertFalse(pilot_record(root/'logs')['ready'])
    def test_run_without_metrics_not_valid_experiment(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);run_pilot([sys.executable,'-c','print(123)'],root,root/'logs',execute=True)
            self.assertFalse(pilot_record(root/'logs')['ready'])
    def test_real_run_logged_but_simple_baseline_equal_triggers_reaudit(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);run_pilot([sys.executable,'-c','print(123)'],root,root/'logs',execute=True)
            mf=root/'scores.json';mf.write_text(json.dumps({'idea_id':'A','revision':1,'metric_name':'accuracy',
                'direction':'higher','baseline':0.65,'proposed':0.65,'dataset_split':'held-out'}))
            r=pilot_record(root/'logs',mf)
            self.assertTrue(r['ready']);self.assertTrue(r['requires_reaudit'])
            (root/'logs'/'stdout.txt').write_text('tampered')
            self.assertFalse(pilot_record(root/'logs',mf)['ready'])
    def test_failed_run_counts_as_negative_evidence(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);run_pilot([sys.executable,'-c','raise SystemExit(1)'],root,root/'logs',execute=True)
            result=pilot_record(root/'logs')
            self.assertTrue(result['ready']);self.assertTrue(result['requires_reaudit'])
            self.assertEqual(result['status'],'FAILED_RUN_DOCUMENTED')
    def test_coverage_report_requires_real_record_before_novelty_promotion(self):
        with tempfile.TemporaryDirectory() as p:
            root=Path(p);main(['init','--project',p])
            state=json.loads((root/'workflow_state.json').read_text());state['stage']='SCOOP'
            (root/'workflow_state.json').write_text(json.dumps(state))
            (root/'novelty_result.json').write_text('{"ready":true}')
            with self.assertRaises(SystemExit):
                main(['advance','--project',p,'--stage','MECHANISM_LOGIC','--reason','missing search'])

    def test_missing_four_search_axes_reported(self):
        result=report({'queries':[{'axis':'same_problem','source':'OpenAlex','query':'x','search_date':'2026-10-08'}]})
        self.assertEqual(result['status'],'COVERAGE_INCOMPLETE')
        self.assertFalse(result['can_claim_novelty_exhaustive'])
    def test_local_ledger_flags_identical_idea(self):
        with tempfile.TemporaryDirectory() as p:
            path=Path(p)/'ledger.jsonl';idea={'idea_id':'one','problem':'P','hypothesis':'H','mechanism':'M','status':'STOP'}
            self.assertEqual(add(path,idea)['duplicate_idea_ids'],[])
            idea['idea_id']='two';self.assertEqual(add(path,idea)['duplicate_idea_ids'],['one'])

if __name__=='__main__':unittest.main()
